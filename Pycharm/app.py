from flask import Flask,render_template, request, redirect, url_for
import pickle
import mysql.connector
from sklearn.preprocessing import MinMaxScaler
import pandas as pd
import numpy as np
import xgboost,catboost

# terminal run cmnd - python app.py

app=Flask(__name__)
# Data-set load
df_diabetes=pd.read_csv(r'C:\Users\KIIT\OneDrive\Desktop\Project\8th_sem\diabetes_df.csv')
df_heart_stroke=pd.read_csv(r'C:\Users\KIIT\OneDrive\Desktop\Project\8th_sem\heart_stroke_df.csv')
df_heart_disease=pd.read_csv(r'C:\Users\KIIT\OneDrive\Desktop\Project\8th_sem\heart_disease.csv')


# Configure MySQL connection
db = mysql.connector.connect(

# Port number: 3306
    host="sql6.freesqldatabase.com",
    user="sql6696841",
    password="hdwDjLTAyn",
    database="sql6696841"
)
cursor = db.cursor()



# minmax-function
def minmax_scale(df,col,value):
    nm=MinMaxScaler()
    nm.fit(df[[col]])
    return nm.transform([[value]])




# Load your trained models
model1_ = pickle.load(open('diabetes_prediction.pkl', 'rb'))
model3_ = pickle.load(open('heart_stroke.pkl', 'rb'))
model2_ = pickle.load(open('heart_disease_xgb.pkl', 'rb'))



@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/after_contact', methods=['POST'])
def after_contact():
    if request.method == 'POST':
        username = str(request.form['email'])
        message = str(request.form['message'])

        # If the username doesn't exist, proceed with registration
        insert_query = "INSERT INTO contact (email,message) VALUES (%s,%s)"
        cursor.execute(insert_query, (username,  message))
        db.commit()

        return render_template('contact.html',
                               pop='Your message has been submitted successfully.')  # Redirect to login page after successful registration

    return render_template('contact.html')


@app.route('/contact')
def contact():
    return render_template('contact.html')




@app.route('/model')
def model():
    return render_template('model.html')

@app.route('/model1')
def model1():
    return render_template('model1.html')

@app.route('/model2')
def model2():
    return render_template('model2.html')

@app.route('/model3')
def model3():
    return render_template('model3.html')



@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')


@app.route('/after_register', methods=['POST'])
def after_register():
    if request.method == 'POST':
        username = str(request.form['username'])
        password = str(request.form['password'])
        firstname = str(request.form['firstname'])
        lastname = str(request.form['lastname'])
        # Check if the username already exists
        query = "SELECT * FROM user WHERE Email = %s"
        cursor.execute(query, (username,))
        existing_user = cursor.fetchone()

        if existing_user:
            return render_template('login.html',
                                   pop='You already have an account. Please Login.')  # Redirect to login page

        # If the username doesn't exist, proceed with registration
        insert_query = "INSERT INTO user (Email, First_name, Last_name, Password) VALUES (%s, %s, %s, %s)"
        cursor.execute(insert_query, (username, firstname, lastname, password))
        db.commit()

        return render_template('login.html',
                               pop='You have been registered successfully')  # Redirect to login page after successful registration

    return render_template('register.html')





@app.route('/after_login', methods=['POST'])
def after_login():
    if request.method == 'POST':
        username = str(request.form['username'])
        password = str(request.form['password'])
        query = "SELECT * FROM user WHERE Email = %s"
        # Create a cursor that returns results as dictionaries
        cursor = db.cursor(dictionary=True)
        cursor.execute(query, (username,))
        user = cursor.fetchone()
        if user:
            # User exists, now check if the password matches
            if user['Password'] == password:
                return redirect(url_for('home', login_success=True))
            else:
                # Password doesn't match
                return render_template('login.html', error=True, message='Incorrect password.')
        else:
            # User not found
            return render_template('login.html', error=True, message='User not found. Please register first ☝️☝️ ')
    return render_template('login.html', error=False)








@app.route('/logout')
def logout():
    return render_template('login.html')






@app.route('/result')
def result():
    return render_template('result.html')






@app.route('/model1_result', methods=['POST'])
def model1_result():
    # diabetes
    if request.method == 'POST':

        pregnancies = int(request.form['pregnancies'])

        glucose = int(request.form['glucose'])

        blood_pressure = int(request.form['bloodPressure'])

        skin_thickness = int(request.form['skinThickness'])

        insulin = int(request.form['insulin'])

        bmi = float(request.form['bmi'])

        diabetes_pedigree_function = float(request.form['diabetesPedigreeFunction'])

        age = int(request.form['age'])

        # -------------------------------- Minmax_scaler ----------------------------------------------

        pregnancies=minmax_scale(df_diabetes, 'Pregnancies', pregnancies)

        glucose=minmax_scale(df_diabetes, 'Glucose', glucose)

        blood_pressure=minmax_scale(df_diabetes, 'BloodPressure', blood_pressure)

        skin_thickness=minmax_scale(df_diabetes, 'SkinThickness', skin_thickness)

        insulin=minmax_scale(df_diabetes, 'Insulin', insulin)

        age=minmax_scale(df_diabetes, 'Age', age)

        bmi=minmax_scale(df_diabetes, 'BMI', bmi)


        inputs = [[pregnancies, glucose, blood_pressure, skin_thickness, insulin, bmi, diabetes_pedigree_function, age]]

        result = model1_.predict(inputs)
        updated_res = result.flatten().astype(int)
        if updated_res == 0:
            return render_template('result.html', result='YOU ARE SAFE',head='Result of Diabetes Prediction model')
        else:
            return render_template('result.html', result='YOU ARE NOT SAFE',head='Result of Diabetes Prediction model')

    else:
        # Render the model.html template for GET requests
        return render_template('model.html')





@app.route('/model2_result', methods=['POST'])
def model2_result():
    # --------------------------  heart disease ----------------------------

    if request.method == 'POST':
        # Retrieving form data
        chest_pain_type = request.form['chest_pain_type']
        resting_blood_pressure = int(request.form['resting_blood_pressure'])
        resting_electrocardiogram = request.form['resting_electrocardiogram']
        st_slope = request.form['st_slope']
        num_major_vessels = request.form['num_major_vessels']
        thalassemia = request.form['thalassemia']

        # Processing form data
        chest_pain_type = process_chest_pain_type(chest_pain_type)
        resting_blood_pressure = process_resting_blood_pressure(resting_blood_pressure)
        resting_electrocardiogram = process_resting_electrocardiogram(resting_electrocardiogram)
        st_slope = process_st_slope(st_slope)
        num_major_vessels = process_num_major_vessels(num_major_vessels)
        thalassemia = process_thalassemia(thalassemia)

        # Predicting result
        inputs = [[chest_pain_type, resting_blood_pressure, resting_electrocardiogram, st_slope, num_major_vessels,
                   thalassemia]]
        result = model2_.predict(inputs)
        updated_res = result.flatten().astype(int)

        # Rendering result
        if updated_res == 0:
            return render_template('result.html', result='YOU ARE SAFE',head='Result of Heart Disease Prediction model')
        else:
            return render_template('result.html', result='YOU ARE NOT SAFE',head='Result of Heart Disease Prediction model')
    else:
        # Render the model.html template for GET requests
        return render_template('model.html')





# Helper functions
def process_chest_pain_type(chest_pain_type):
    if chest_pain_type == 'typical angina':
        return 0
    elif chest_pain_type == 'atypical angina':
        return 1
    elif chest_pain_type == 'non-anginal angina':
        return 2
    else:
        return 3

def process_resting_blood_pressure(resting_blood_pressure):
    if resting_blood_pressure < 140:
        return 2
    if resting_blood_pressure < 160:
        return 1
    else:
        return 0

def process_resting_electrocardiogram(resting_electrocardiogram):
    if resting_electrocardiogram == 'normal':
        return 0
    if resting_electrocardiogram == 'ST-T wave abnormality':
        return 1
    else:
        return 2

def process_st_slope(st_slope):
    if st_slope == 'upsloping':
        return 0
    if st_slope == 'flat':
        return 1
    else:
        return 2

def process_num_major_vessels(num_major_vessels):
    return int(num_major_vessels)

def process_thalassemia(thalassemia):
    if thalassemia == 'error':
        return 0
    if thalassemia == 'fixed defect':
        return 1
    if thalassemia == 'normal':
        return 2
    else:
        return 3







@app.route('/model3_result', methods=['POST'])
def model3_result():
     #------------------------ heart stroke ----------------------------

    if request.method == 'POST':
        # Process the form submission
        age = int(request.form['age'])
        hypertension = int(request.form['hypertension'])
        heart_disease = request.form['heart_disease']  # No need to convert to int
        avg_glucose_level = float(request.form['avg_glucose_level'])
        bmi = float(request.form['bmi'])
        gender = request.form['gender']  # No need to convert to int
        ever_married = request.form['ever_married']  # No need to convert to int
        work_type = request.form['work_type']  # No need to convert to int
        residence_type = request.form['residence_type']  # Corrected variable name
        smoking_status = request.form['smoking_status']  # No need to convert to int






        # Min-max scaling for numeric variables
        age = minmax_scale(df_heart_stroke, 'age', age)
        avg_glucose_level = minmax_scale(df_heart_stroke, 'avg_glucose_level', avg_glucose_level)
        bmi = minmax_scale(df_heart_stroke, 'bmi', bmi)

        # Encoding categorical variables
        gender_Male = 1 if gender == 'Male' else 0
        gender_Other = 0

        heart_disease = 1 if heart_disease == 'yes' else 0


        ever_married_Yes = 1 if ever_married == 'yes' else 0

        if work_type == 'Never work':
            work_type_Never_worked, work_type_Private, work_type_Self_employed = 1, 0, 0
        elif work_type == 'Private':
            work_type_Never_worked, work_type_Private, work_type_Self_employed = 0, 1, 0
        else:
            work_type_Never_worked, work_type_Private, work_type_Self_employed = 0, 0, 1

        residence_type_Urban = 1 if residence_type == 'Urban' else 0

        if smoking_status == 'Few times':
            smoking_status_formerly_smoked, smoking_status_never_smoked, smoking_status_smokes = 1, 0, 0
        elif smoking_status == 'Never':
            smoking_status_formerly_smoked, smoking_status_never_smoked, smoking_status_smokes = 0, 1, 0
        else:
            smoking_status_formerly_smoked, smoking_status_never_smoked, smoking_status_smokes = 0, 0, 1

        inputs = [[age, hypertension, heart_disease, avg_glucose_level, bmi, gender_Male, gender_Other, ever_married_Yes,
                   work_type_Never_worked, work_type_Private, work_type_Self_employed,
                   residence_type_Urban, smoking_status_formerly_smoked, smoking_status_never_smoked,
                   smoking_status_smokes]]

        result = model3_.predict(inputs)
        updated_res = result.flatten().astype(int)




        if updated_res == 0:
            return render_template('result.html', result='YOU ARE SAFE.',result2=' OUR MODEL SAYS YOU ARE RISK-FREE FROM HEART STROKE FOR NOW 👍👍',head='Result of Heart Stroke Prediction model')
        else:
            return render_template('result.html', result='YOU ARE NOT SAFE.',result2=' OUR MODEL SAYS YOU HAVE A BIG RISK OF HEART STROKE ☠️💀☠️',head='Result of Heart Stroke Prediction model')

    else:
        # Render the model.html template for GET requests
        return render_template('model.html')

















if __name__=='__main__':
    app.run(debug=True)