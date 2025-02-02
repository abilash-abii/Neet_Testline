# Personalized Student Recommendations for NEET Exam Preparation

## Overview
The **Personalized Student Recommendations** project analyzes student quiz performance and provides tailored recommendations to enhance preparation for the NEET exams. By processing quiz data from multiple APIs, the project identifies weak areas, tracks improvement trends, and pinpoints performance gaps. These insights enable students to focus on specific topics, question types, and difficulty levels for more effective and efficient study.

## Project Features
- **Fetch data from three APIs**:
  - **Current Quiz Data**: Details of the most recent quiz submission.
  - **Submission Data**: User's quiz responses.
  - **Historical Quiz Data**: Data from the last 5 quizzes.

- **Analyze performance by**:
  - Topics
  - Difficulty levels
  - Response accuracy

- **Generate visualizations to identify**:
  - Weak areas
  - Improvement trends
  - Specific performance gaps

- **Offer personalized recommendations** based on insights.

## Bonus Features:
- **Define student personas** and predict NEET rank using probabilistic modeling based on quiz performance.

---

## Setup Instructions

### Prerequisites:
Ensure you have the following installed:
- **Python 3.7** or above
- **pip** (Python package manager)

### Install Required Libraries:
To install the necessary libraries, run the following command:

```javascript
pip install requests pandas numpy seaborn matplotlib scikit-learn
```

## API Endpoints:
The script fetches data from the following APIs:

1. **Current Quiz Data**:
   - **Quiz Endpoint**: [https://jsonkeeper.com/b/LLQT](https://jsonkeeper.com/b/LLQT)
   - Provides data for the most recent quiz submission, including the questions, answers, and responses.

2. **Submission Data**:
   - **Quiz Submission**: [http://api.jsonserve.com/rJvd7g](http://api.jsonserve.com/rJvd7g)
   - Provides data about the user's quiz responses, including performance metrics such as correct answers, mistakes, and response time.

3. **Historical Quiz Data**:
   - **API Endpoint**: [http://api.jsonserve.com/XgAgFJ](http://api.jsonserve.com/XgAgFJ)
   - Contains data from the last 5 quizzes to help analyze performance trends over time.

---

## Run the Script:
Run the script by executing the following in your terminal:
```javascript
python Neet_Testline.py
```

The script will fetch data from the APIs, process it, and generate insights in the form of visualizations.

## Approach

The overall approach consists of the following steps:

### 1. Data Collection

The script collects data from three API endpoints, including:

- **Current Quiz Data:** Provides details about the latest quiz, including questions, answers, and responses.
- **Submission Data:** Includes performance metrics of the user's quiz responses.
- **Historical Quiz Data:** Contains data for the last 5 quizzes, which is used to analyze trends and performance evolution over time.

### 2. Data Cleaning

Missing values are handled by filling numerical columns with the mean of the column. This ensures that the analysis is not biased by missing data and guarantees smooth processing and reliable insights.

### 3. Exploratory Data Analysis (EDA)

The data is analyzed for patterns and trends related to:
- **Topics** (areas of focus)
- **Difficulty Levels**
- **Response Accuracy**

This helps identify areas where the student is performing well and areas where improvement is needed.

### 4. Visualizations

The script generates four key visualizations to provide insights into student performance:

- **Score Distribution:** Displays the overall distribution of quiz scores, helping identify trends in student performance.
- **Trophy Level Distribution:** Shows the distribution of trophy levels, offering insight into how students are performing relative to each other.
- **Accuracy Distribution:** Analyzes how accurately students answer questions, providing insights into the quiz’s difficulty.
- **Rank Distribution:** Displays the rank distribution to help students understand their relative performance among peers.

### 5. Personalized Recommendations

Based on the insights from the visualizations, the script provides actionable recommendations for students, such as:
- Focusing on specific topics or question types.
- Adjusting study strategies based on difficulty levels.

### 6. Predictive Modeling (Bonus)

A probabilistic model predicts the student's NEET rank based on quiz performance and historical data from previous years. This feature is optional and enhances the overall functionality of the script.

## Project Components

### 1. **Data Fetching**
   - The script uses the `requests` library to fetch data from API endpoints. 
   - The fetched data is then processed into Pandas DataFrames to facilitate easy manipulation and analysis.

### 2. **Data Cleaning**
   - Missing values in the dataset are filled with the mean of numerical columns. 
   - This helps to prevent bias in the analysis that could arise from incomplete data.

### 3. **Data Analysis**
   - The script utilizes `seaborn` and `matplotlib` libraries for data visualization.
   - Key metrics such as score, trophy levels, accuracy, and rank are analyzed to offer insights into student performance.
   - Visualizations help identify trends and patterns, providing a clearer understanding of student progress and areas of improvement.

### 4. **Modeling**
   - An optional feature of the project includes a Linear Regression model, which predicts a student's NEET rank based on their quiz performance data.
   - This section of the project demonstrates how predictive modeling can be applied to educational data to provide more targeted advice for students.

### 5. **Conclusion**
   - The project provides a comprehensive solution for analyzing and predicting student performance in preparation for the NEET exam.
   - By utilizing data science techniques such as data cleaning, exploratory data analysis, visualizations, and predictive modeling, this solution offers personalized recommendations and valuable insights into student progress.

---

## Requirements

- Python 3.x
- Libraries:
  - `requests`
  - `pandas`
  - `numpy`
  - `seaborn`
  - `matplotlib`
  - `sklearn` (for the regression model)
