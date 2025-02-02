# Import necessary libraries
import requests  # Used to make HTTP requests to fetch data from APIs
import urllib3  # A library for working with HTTP, used here to disable SSL warnings
import json  # For handling JSON data
import numpy as np  # For numerical operations, particularly with arrays
import pandas as pd  # For data manipulation and working with DataFrames
import seaborn as sns  # For creating statistical data visualizations
import matplotlib.pyplot as plt  # For creating various plots
from sklearn.model_selection import train_test_split  # For splitting the dataset into training and testing sets
from sklearn.linear_model import LinearRegression  # For linear regression modeling
from sklearn.metrics import mean_squared_error  # For calculating performance metrics of models

# Disable SSL warnings related to insecure HTTP connections
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Define URLs to fetch the quiz data from APIs
current_quiz_url = "https://jsonkeeper.com/b/LLQT"  # URL for current quiz data
submission_url = "http://api.jsonserve.com/rJvd7g"  # URL for submission data
historical_quiz_url = "http://api.jsonserve.com/XgAgFJ"  # URL for historical quiz data

# Function to fetch data from an API endpoint
def fetch_data(url):
    try:
        # Make a GET request to the provided URL, disabling SSL verification
        response = requests.get(url, verify=False)
        response.raise_for_status()  # Raise an exception if the HTTP request was not successful (e.g., 404, 500)
        return response.json()  # Return the JSON data from the response
    except requests.exceptions.RequestException as err:
        # If an error occurs during the request, print the error and return None
        print(f"Error fetching data from {url}: {err}")
        return None

# Fetch data from each API URL
current_quiz_data = fetch_data(current_quiz_url)  # Fetch current quiz data
submission_data = fetch_data(submission_url)  # Fetch submission data
historical_quiz_data = fetch_data(historical_quiz_url)  # Fetch historical quiz data

# Check if any data was not fetched successfully and raise an error if so
if current_quiz_data is None or submission_data is None or historical_quiz_data is None:
    raise ValueError("One or more datasets could not be fetched. Please check the API URLs.")

# Convert the fetched JSON data into Pandas DataFrames for easier manipulation
current_quiz_df = pd.DataFrame(current_quiz_data)  # Convert current quiz data to a DataFrame
submission_df = pd.json_normalize(submission_data)  # Normalize submission data if it contains nested structures
historical_quiz_df = pd.DataFrame(historical_quiz_data)  # Convert historical quiz data to a DataFrame

# Print a preview of the fetched data to check if it's correct
print("Current Quiz Data:")
print(current_quiz_df.head(5))  # Print first 5 rows of current quiz data
print("\nSubmission Data:")
print(submission_df.head(5))  # Print first 5 rows of submission data
print("\nHistorical Quiz Data:")
print(historical_quiz_df.head(5))  # Print first 5 rows of historical quiz data

# Check for any missing values in the data
print("Current Quiz Data Missing Values:")
print(current_quiz_df.isnull().sum())  # Count missing values in each column of current quiz data

print("Historical Quiz Data Missing Values:")
print(historical_quiz_df.isnull().sum())  # Count missing values in each column of historical quiz data

# Fill missing numerical values with the mean of their respective columns
# For current quiz data, fill missing values in columns with numerical types
for col in current_quiz_df.columns:
    if current_quiz_df[col].dtype in ['int64', 'float64']:  # Check if the column is numerical
        current_quiz_df[col] = current_quiz_df[col].fillna(current_quiz_df[col].mean())  # Fill missing with column mean

# Similarly, fill missing values in historical quiz data
for col in historical_quiz_df.columns:
    if historical_quiz_df[col].dtype in ['int64', 'float64']:  # Check if the column is numerical
        historical_quiz_df[col] = historical_quiz_df[col].fillna(historical_quiz_df[col].mean())  # Fill missing with column mean

# Check the data types of each column in both datasets
print("Data types of current quiz data:")
print(current_quiz_df.dtypes)  # Print data types of columns in current quiz data
print("Data types of historical quiz data:")
print(historical_quiz_df.dtypes)  # Print data types of columns in historical quiz data

# Example: Add a new column to indicate if the answer was correct (assuming we have 'correct_option' and 'selected_option')
if 'selected_option' in current_quiz_df.columns and 'correct_option' in current_quiz_df.columns:
    # Add a new column 'correct_answer' that is 1 if the selected option matches the correct option, else 0
    current_quiz_df['correct_answer'] = current_quiz_df.apply(
        lambda row: 1 if row['selected_option'] == row['correct_option'] else 0, axis=1
    )
    # Print the updated DataFrame with the new 'correct_answer' column
    print(current_quiz_df[['question_id', 'correct_option', 'selected_option', 'correct_answer']].head())
else:
    print("Error: 'selected_option' or 'correct_option' column does not exist")

# Visualizations based on available columns in historical quiz data

# Set the visualization style to a clean grid
sns.set(style="whitegrid")

# 1. Visualize the distribution of scores (if 'score' column exists)
if 'score' in historical_quiz_df.columns:
    plt.figure(figsize=(10, 6))  # Create a figure with specified size
    sns.histplot(historical_quiz_df['score'], kde=True, color='blue', bins=15)  # Plot histogram with KDE
    plt.title('Distribution of Scores in Historical Quiz Data', fontsize=16)  # Title of the plot
    plt.xlabel('Score', fontsize=12)  # Label for the x-axis
    plt.ylabel('Frequency', fontsize=12)  # Label for the y-axis
    plt.show()  # Display the plot
else:
    print("No 'score' column available. Displaying missing value counts instead.")
    # If the 'score' column is not present, display a heatmap for missing values
    sns.heatmap(historical_quiz_df.isnull(), cbar=False, cmap='Blues')  # Visualize missing values as a heatmap
    plt.title('Missing Data Heatmap', fontsize=16)  # Title for the heatmap
    plt.show()

# 2. Visualize the distribution of trophy levels (if 'trophy_level' column exists)
if 'trophy_level' in historical_quiz_df.columns:
    plt.figure(figsize=(10, 6))  # Create a figure with specified size
    sns.countplot(x='trophy_level', data=historical_quiz_df, palette='viridis')  # Create a count plot for trophy levels
    plt.title('Distribution of Trophy Levels', fontsize=16)  # Title of the plot
    plt.xlabel('Trophy Level', fontsize=12)  # Label for the x-axis
    plt.ylabel('Count', fontsize=12)  # Label for the y-axis
    plt.show()  # Display the plot
else:
    print("No 'trophy_level' column available. Displaying missing value counts instead.")
    sns.heatmap(historical_quiz_df.isnull(), cbar=False, cmap='Blues')  # Visualize missing values as a heatmap
    plt.title('Missing Data Heatmap', fontsize=16)  # Title for the heatmap
    plt.show()

# 3. Visualize accuracy distribution (if 'accuracy' column exists)
if 'accuracy' in historical_quiz_df.columns:
    historical_quiz_df['accuracy_numeric'] = historical_quiz_df['accuracy'].replace({'%': '', ' ': ''}, regex=True).astype(float)  # Clean and convert accuracy to numeric values
    plt.figure(figsize=(10, 6))  # Create a figure with specified size
    sns.histplot(historical_quiz_df['accuracy_numeric'], kde=True, color='green', bins=15)  # Plot histogram with KDE for accuracy
    plt.title('Distribution of Accuracy Percentages', fontsize=16)  # Title of the plot
    plt.xlabel('Accuracy (%)', fontsize=12)  # Label for the x-axis
    plt.ylabel('Frequency', fontsize=12)  # Label for the y-axis
    plt.show()  # Display the plot
else:
    print("No 'accuracy' column available. Displaying missing value counts instead.")
    sns.heatmap(historical_quiz_df.isnull(), cbar=False, cmap='Blues')  # Visualize missing values as a heatmap
    plt.title('Missing Data Heatmap', fontsize=16)  # Title for the heatmap
    plt.show()

# 4. Visualize rank distribution (if 'rank_text' column exists)
if 'rank_text' in historical_quiz_df.columns:
    historical_quiz_df['rank_numeric'] = historical_quiz_df['rank_text'].str.extract('(-?\\d+)').astype(float)  # Extract and convert numeric ranks from 'rank_text'
    plt.figure(figsize=(10, 6))  # Create a figure with specified size
    sns.histplot(historical_quiz_df['rank_numeric'], kde=True, color='orange', bins=15)  # Plot histogram for ranks
    plt.title('Distribution of Rank (Numeric)', fontsize=16)  # Title of the plot
    plt.xlabel('Rank', fontsize=12)  # Label for the x-axis
    plt.ylabel('Frequency', fontsize=12)  # Label for the y-axis
    plt.show()  # Display the plot
else:
    print("No 'rank_text' column available. Displaying missing value counts instead.")
    sns.heatmap(historical_quiz_df.isnull(), cbar=False, cmap='Blues')  # Visualize missing values as a heatmap
    plt.title('Missing Data Heatmap', fontsize=16)  # Title for the heatmap
    plt.show()

# Function to analyze data by various categories and performance metrics
def analyze_data(current_quiz_df, historical_quiz_df):
    # Explore the schema (data types) of both datasets
    print("Current Quiz Data Schema:")
    print(current_quiz_df.dtypes)  # Print data types of current quiz data columns
    print("\nHistorical Quiz Data Schema:")
    print(historical_quiz_df.dtypes)  # Print data types of historical quiz data columns

    # Analyze performance by topic if 'topic' column exists
    if 'topic' in historical_quiz_df.columns:
        topic_performance = historical_quiz_df.groupby('topic')['score'].mean()  # Group by topic and calculate the average score
        print("\nTopic Performance:")
        print(topic_performance)  # Print the performance by topic
        plt.figure(figsize=(10, 6))  # Create a figure with specified size
        sns.barplot(x=topic_performance.index, y=topic_performance.values, palette="Blues_d")  # Plot bar chart for topic performance
        plt.title('Performance by Topic', fontsize=16)  # Title of the plot
        plt.xlabel('Topic', fontsize=12)  # Label for the x-axis
        plt.ylabel('Average Score', fontsize=12)  # Label for the y-axis
        plt.xticks(rotation=45)  # Rotate x-axis labels by 45 degrees
        plt.show()  # Display the plot
    else:
        print("Error: 'topic' column does not exist")

    # Analyze performance by difficulty level if 'difficulty_level' column exists
    if 'difficulty_level' in historical_quiz_df.columns:
        difficulty_performance = historical_quiz_df.groupby('difficulty_level')['score'].mean()  # Group by difficulty level and calculate the average score
        print("\nDifficulty Performance:")
        print(difficulty_performance)  # Print the performance by difficulty level
        plt.figure(figsize=(10, 6))  # Create a figure with specified size
        sns.barplot(x=difficulty_performance.index, y=difficulty_performance.values, palette="viridis")  # Plot bar chart for difficulty level performance
        plt.title('Performance by Difficulty Level', fontsize=16)  # Title of the plot
        plt.xlabel('Difficulty Level', fontsize=12)  # Label for the x-axis
        plt.ylabel('Average Score', fontsize=12)  # Label for the y-axis
        plt.xticks(rotation=45)  # Rotate x-axis labels by 45 degrees
        plt.show()  # Display the plot
    else:
        print("Error: 'difficulty_level' column does not exist")

    # Analyze performance by response accuracy if 'response_accuracy' column exists
    if 'response_accuracy' in historical_quiz_df.columns:
        accuracy_performance = historical_quiz_df.groupby('response_accuracy')['score'].mean()  # Group by accuracy and calculate the average score
        print("\nAccuracy Performance:")
        print(accuracy_performance)  # Print the performance by accuracy
        plt.figure(figsize=(10, 6))  # Create a figure with specified size
        sns.lineplot(x=accuracy_performance.index, y=accuracy_performance.values, marker='o', color='orange')  # Plot line chart for accuracy performance
        plt.title('Performance by Accuracy', fontsize=16)  # Title of the plot
        plt.xlabel('Accuracy', fontsize=12)  # Label for the x-axis
        plt.ylabel('Average Score', fontsize=12)  # Label for the y-axis
        plt.show()  # Display the plot
    else:
        print("Error: 'response_accuracy' column does not exist")

# Call the function to analyze and visualize the data
analyze_data(current_quiz_df, historical_quiz_df)
