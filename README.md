# Health_Risk_Analyzer

This is a Flask-based web application for predicting diabetes, heart disease, and heart stroke using machine learning models.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)

## Introduction

This web application uses trained machine learning models to predict the likelihood of diabetes, heart disease, and heart stroke based on user inputs. The models are implemented using various libraries including `xgboost` and `catboost`.

## Features

- Predicts the likelihood of diabetes, heart disease, and heart stroke.
- User authentication and message submission.
- Connects to a MySQL database for storing user data and messages.

## Installation

### Prerequisites

- Python 3.x
- MySQL server
- Required Python packages listed in `requirements.txt`

### Steps

1. **Clone the repository**:
   ```sh
   git clone https://github.com/romantalukdar346/Health_Risk_Analyzer.git
   cd Health_Risk_Analyzer
   
2. **Create and activate a virtual environment**:
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`

3. **Install dependencies**:
   ```sh
   pip install -r requirements.txt

4. **Configure the MySQL database**:
   
   - Ensure your MySQL server is running and accessible. Update the database configuration in `app.py` if necessary:
   ```sh
   db = mysql.connector.connect(
    host="sql6.freesqldatabase.com",
    user="sql6696841",
    password="hdwDjLTAyn",
    database="sql6696841"
)


5. **Run the application**:
   
   `python app.py`

**Website OverView**

![Alt Image](https://github.com/romantalukdar346/Health_Risk_Analyzer/blob/main/Image/Picture1.png)
![Alt Image](https://github.com/romantalukdar346/Health_Risk_Analyzer/blob/main/Image/Picture2.png)
![Alt Image](https://github.com/romantalukdar346/Health_Risk_Analyzer/blob/main/Image/Picture3.png)
![Alt Image](https://github.com/romantalukdar346/Health_Risk_Analyzer/blob/main/Image/Picture4.png)
![Alt Image](https://github.com/romantalukdar346/Health_Risk_Analyzer/blob/main/Image/Picture5.png)
![Alt Image](https://github.com/romantalukdar346/Health_Risk_Analyzer/blob/main/Image/Picture6.png)
![Alt Image](https://github.com/romantalukdar346/Health_Risk_Analyzer/blob/main/Image/Picture7.png)
![Alt Image](https://github.com/romantalukdar346/Health_Risk_Analyzer/blob/main/Image/Picture8.png)


### Usage
1. **Access the application:**
 - Open your browser and navigate to `http://localhost:5000`

2. **Navigate through the application:**

- Home: `http://localhost:5000/`
- About: `http://localhost:5000/about`
- Contact: `http://localhost:5000/contact`
- Model Selection: `http://localhost:5000/model`
- Login: `http://localhost:5000/login`
- Register: `http://localhost:5000/register`

3. **Model Predictions:**

  - Diabetes Prediction: Fill out the form at `http://localhost:5000/model1 and submit to get results`.
  - Heart Disease Prediction: Fill out the form at `http://localhost:5000/model2 and submit to get results`.
  - Heart Stroke Prediction: Fill out the form at `http://localhost:5000/model3 and submit to get results`.



