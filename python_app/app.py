import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import numpy as np
from utils.data_loader import (
    load_survey_data,
    process_demographic_data,
    get_survey_questions,
    get_survey_responses
)
from utils.visualization import (
    create_demographic_bar_plot,
    create_demographic_pie_plot,
    create_survey_response_plot,
    create_proportion_plot,
    create_adjective_rating_plot
)

# Set page config
st.set_page_config(
    page_title="DEI in Tech Climate Survey Interactive Report",
    page_icon="📊",
    layout="wide"
)

# Constants
VARIABLE_OPTIONS = {
    "Gender": "gender",
    "Race": "race",
    "First Gen": "first_gen",
    "International": "international",
    "Major": "major",
    "Preparedness": "prep",
    "Work Status": "work_status",
    "None": "none"
}

# Load data
@st.cache_data
def load_data():
    """Load and prepare the survey data"""
    try:
        # Get the absolute path to the data file
        current_dir = Path(__file__).parent
        data_path = current_dir / "data" / "survey_data.csv"
        
        if not data_path.exists():
            st.error(f"Survey data not found at {data_path}. Please ensure the data file exists.")
            return None
            
        # Try to read the file
        try:
            return pd.read_csv(data_path)
        except Exception as e:
            st.error(f"Error reading data file: {str(e)}")
            return None
            
    except Exception as e:
        st.error(f"Error in load_data: {str(e)}")
        return None

def show_demographic_section(data, category):
    """Display demographic section with plots and tables"""
    st.subheader(category.title())
    
    # Process data
    demographic_data = process_demographic_data(data, VARIABLE_OPTIONS[category])
    if demographic_data is None:
        st.error(f"Could not process {category} data")
        return
    
    # Create plots
    col1, col2 = st.columns(2)
    
    with col1:
        fig_bar = create_demographic_bar_plot(
            demographic_data,
            category,
            f"{category.title()} Distribution"
        )
        st.plotly_chart(fig_bar, use_container_width=True)
    
    with col2:
        fig_pie = create_demographic_pie_plot(
            demographic_data,
            category,
            f"{category.title()} Distribution"
        )
        st.plotly_chart(fig_pie, use_container_width=True)
    
    # Display table
    st.dataframe(demographic_data, use_container_width=True)

def show_survey_report():
    """Display the survey report page"""
    st.header("Survey Report")
    
    # Load data
    data = load_data()
    if data is None:
        return
    
    # Executive Summary
    st.subheader("Executive Summary")
    st.write("""
    The purpose of the DEI in Tech Climate Survey was to assess the climate of tech departments at Boston University 
    and begin to fill that data gap. Areas across the university are determining new goals and policies to address 
    inequity, and the data gathered here is meant to contribute to the evidence-based formation of effective initiatives.
    """)
    
    # Respondent Demographics
    st.subheader("Respondent Demographics")
    st.write(f"Total responses: {len(data)}")
    
    # Show demographic sections
    for category in ["Gender", "Race", "First Gen", "Major", "International"]:
        show_demographic_section(data, category)
    
    # Course and Department Satisfaction
    st.subheader("Course and Department Satisfaction")
    st.write("""
    The course satisfaction section asked respondents to identify their level of satisfaction with instructional 
    support (support from professors) in classes within their major. For a particular class, a student indicates 
    they are extremely satisfied, somewhat satisfied, neither satisfied or dissatisfied, somewhat dissatisfied, 
    extremely dissatisfied, or did not take that course.
    """)
    
    # Agreement with Experiences
    st.subheader("Agreement with Experiences")
    st.write("""
    The agreement with experiences section asked respondents to identify their level of agreement with various 
    experiences by selecting an option of strongly disagree, disagree, agree, and strongly agree.
    """)

def show_build_a_graph():
    """Display the Build-a-Graph page"""
    st.header("Build-a-Graph")
    
    # Load data
    data = load_data()
    if data is None:
        return
    
    # Debug: Show data structure
    if st.checkbox("Show data structure"):
        st.write("First few rows of data:")
        st.write(data.head())
        st.write("\nColumn names:")
        st.write(data.columns.tolist())
    
    # Question type selection
    question_type = st.selectbox(
        "Select question type",
        ["Agreement", "Adjectives", "Course Satisfaction", "Discrimination"]
    )
    
    # Get questions for selected type
    questions = get_survey_questions(question_type)
    if not questions:
        st.error("No questions available for selected type")
        return
    
    # Question selection
    selected_question = st.selectbox("Select question", questions)
    
    # Debug: Show matching columns
    matching_cols = [col for col in data.columns if selected_question.lower() in col.lower()]
    if matching_cols:
        st.write(f"Found matching columns: {matching_cols}")
    
    # Variable selection for grouping
    variable = st.selectbox(
        "Select variable for breakdown (optional)",
        ["None"] + list(VARIABLE_OPTIONS.keys())
    )
    
    # Get responses
    variable_value = None if variable == "None" else VARIABLE_OPTIONS[variable]
    responses = get_survey_responses(data, selected_question, variable_value)
    
    if responses is None or responses.empty:
        st.error("No responses available for the selected question")
        st.write("Debug info:")
        st.write(f"Selected question: {selected_question}")
        st.write(f"Variable value: {variable_value}")
        return
    
    # Create plots
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Response Counts")
        fig_count = create_survey_response_plot(responses, selected_question, variable_value)
        st.plotly_chart(fig_count, use_container_width=True)
    
    with col2:
        st.subheader("Response Proportions")
        fig_prop = create_proportion_plot(responses, selected_question, variable_value)
        st.plotly_chart(fig_prop, use_container_width=True)
    
    # Display data table
    st.subheader("Response Data")
    st.dataframe(responses, use_container_width=True)

def show_welcome_page():
    """Display the welcome page"""
    st.header("Welcome to the 2022 DEI in Tech Climate Survey Report")
    
    st.write("""
    This report is brought to you by the DEI Tech Collective.
    The Collective is an opportunity for BU tech and computing groups to unite around efforts to educate each other
    and address inequity issues within the community.
    """)
    
    st.markdown("[DEI Tech Collective website](https://sites.bu.edu/dei-in-tech/)")
    
    st.subheader("What is the DEI in Tech Climate Survey?")
    st.write("""
    The DEI in Tech Climate Survey was curated by Shateva Long (CAS '23) and was administered in the Spring of 2022 
    by the BU DEI Tech Collective. The purpose of this survey was to assess the climate of tech departments at Boston 
    University and begin to fill that data gap.
    """)
    
    st.subheader("What can I do on this site?")
    st.write("""
    Navigate to the "Survey Report" tab to view the entire Climate Survey Report. This page includes:
    - Additional survey background details
    - BU population data overview
    - Display of respondent demographics
    - Explanations of survey sections and accompanying trends
    - Disclaimers and challenges to be aware of
    """)
    
    st.write("""
    Navigate to the "Build-a-Graph" tab to interact with the data yourself. Here you can select specific questions 
    from the survey and filter by variables to better understand how different types of students responded.
    """)

def main():
    st.title("DEI in Tech Climate Survey Interactive Report")
    
    # Sidebar navigation
    page = st.sidebar.selectbox(
        "Navigation",
        ["Welcome", "Survey Report", "Build-a-Graph"]
    )
    
    if page == "Welcome":
        show_welcome_page()
    elif page == "Survey Report":
        show_survey_report()
    else:
        show_build_a_graph()

if __name__ == "__main__":
    main() 