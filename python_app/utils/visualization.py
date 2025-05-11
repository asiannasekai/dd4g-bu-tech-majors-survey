import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

def create_demographic_bar_plot(data, category, title):
    """
    Create a bar plot for demographic data
    """
    fig = px.bar(data, x='category', y='count', title=title)
    fig.update_layout(xaxis_title=category, yaxis_title='Count')
    return fig

def create_demographic_pie_plot(data, category, title):
    """
    Create a pie plot for demographic data
    """
    fig = px.pie(data, values='count', names='category', title=title)
    return fig

def create_survey_response_plot(data, question, variable=None):
    """
    Create a plot for survey responses
    """
    if 'variable' in data.columns:
        # Grouped data
        fig = px.bar(data, x='response', y='count', color='variable',
                    title=f'Responses for {question} by {variable}',
                    barmode='group')
    else:
        # Ungrouped data
        fig = px.bar(data, x='response', y='count',
                    title=f'Responses for {question}')
    return fig

def create_proportion_plot(data, question, variable=None):
    """
    Create a proportion plot for survey responses
    """
    if 'variable' in data.columns:
        # Calculate proportions for grouped data
        total_by_variable = data.groupby('variable')['count'].transform('sum')
        data['proportion'] = data['count'] / total_by_variable
        
        fig = px.bar(data, x='response', y='proportion', color='variable',
                    title=f'Proportion of Responses for {question} by {variable}',
                    barmode='group')
    else:
        # Calculate proportions for ungrouped data
        total = data['count'].sum()
        data['proportion'] = data['count'] / total
        
        fig = px.bar(data, x='response', y='proportion',
                    title=f'Proportion of Responses for {question}')
    
    fig.update_layout(yaxis_title='Proportion')
    return fig

def create_adjective_rating_plot(data, question):
    """
    Create a box plot for adjective ratings
    """
    fig = px.box(data, y=question, title=f'Distribution of Ratings for {question}')
    return fig 