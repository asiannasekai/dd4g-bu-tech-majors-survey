import pandas as pd
import numpy as np
from pathlib import Path

def load_survey_data(file_path):
    """
    Load and process the survey data from CSV files
    """
    try:
        return pd.read_csv(file_path)
    except Exception as e:
        print(f"Error loading data: {e}")
        return None

def clean_data(df):
    """
    Clean and preprocess the survey data
    """
    if df is None:
        return None
    # Remove any rows with all NaN values
    df = df.dropna(how='all')
    
    # Fill missing demographic values with 'Not Specified'
    demographic_fields = ['gender', 'race', 'first_gen', 'major', 'international']
    for field in demographic_fields:
        if field in df.columns:
            df[field] = df[field].fillna('Not Specified')
    
    return df

def process_demographic_data(df, category):
    """
    Process demographic data for visualization
    """
    if df is None or category not in df.columns:
        return pd.DataFrame({'category': [], 'count': []})
    counts = df[category].value_counts().reset_index()
    counts.columns = ['category', 'count']
    return counts

def get_survey_questions(question_type):
    """
    Get survey questions based on type
    """
    questions = {
        'Agreement': [
            'Q28_2',  # Professors care about me
            'Q30_2',  # I feel like I'll be judged by my peers if I make a mistake
            'Q32_6',  # I feel like an outsider
            'Q33_1',  # I am satisfied with the social climate at my major's department
            'Q33_4'   # I am treated fairly and equitably by staff in my major
        ],
        'Adjectives': [
            'Q24_1',  # Hostile - Friendly
            'Q24_3',  # Homogenous - Diverse
            'Q24_7',  # Competitive - Collaborative
            'Q24_12', # Elitist - Non-elitist
            'Q24_13'  # Individualistic - Collaborative
        ],
        'Course Satisfaction': [
            'Q11_1',  # CS111
            'Q11_2',  # CS112
            'Q11_3',  # CS131
            'Q11_4',  # CS210
            'Q11_5'   # CS330
        ],
        'Discrimination': [
            'Q36',    # Have you ever experienced discrimination...
            'Q38'     # Have you ever witnessed discrimination...
        ]
    }
    return questions.get(question_type, [])

def get_survey_responses(df, question, variable=None):
    """
    Get survey responses for a specific question, optionally grouped by a variable
    """
    if df is None:
        return pd.DataFrame({'response': [], 'count': []})
    
    # Find the exact column in the dataframe
    if question in df.columns:
        question_col = question
    else:
        # Try to find a matching column
        matching_columns = [col for col in df.columns if question.lower() in col.lower()]
        if not matching_columns:
            print(f"No matching column found for question: {question}")
            return pd.DataFrame({'response': [], 'count': []})
        question_col = matching_columns[0]
    
    if variable and variable != 'none' and variable in df.columns:
        # Group by variable and response
        responses = df.groupby([variable, question_col]).size().reset_index(name='count')
        responses.columns = ['variable', 'response', 'count']
    else:
        # Count responses without grouping
        responses = df[question_col].value_counts().reset_index()
        responses.columns = ['response', 'count']
    
    # Clean up response values
    responses['response'] = responses['response'].fillna('No Response')
    responses = responses[responses['response'] != 'No Response']
    
    # Sort responses by count in descending order
    responses = responses.sort_values('count', ascending=False)
    
    return responses 