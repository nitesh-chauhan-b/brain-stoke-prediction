from flask import Flask, render_template, redirect, request, session, url_for, flash
from flask_session import Session
from flask_pymongo import PyMongo
from datetime import datetime
import json
import hashlib

with open('config.json', 'r') as c:
    params = json.load(c)["params"]

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = True
app.config["SESSION_TYPE"] = "filesystem"

import pickle

filename = 'brain_stroke.sav'
loaded_model = pickle.load(open(filename, 'rb'))

filename1 = 'normalized_brain_stroke.sav'
loaded_model2 = pickle.load(open(filename1, 'rb'))

# Function to generate an MD5 hash
def generate_md5_hash(text):
    md5_hash = hashlib.md5()
    md5_hash.update(text.encode('utf-8'))
    return md5_hash.hexdigest()

# Function to verify an MD5 hash
def verify_md5_hash(text, hash_to_check):
    generated_hash = generate_md5_hash(text)
    return generated_hash == hash_to_check

def validate_password(password):
    if len(password) < 8:
        return 'Password must be at least 8 characters long'
    
    if not any(c.isnumeric() for c in password) and not any(not c.isalnum() for c in password):
        return 'Password must contain at least one number and one special character'
    
    if not any(c.isnumeric() for c in password):
       return 'Password must contain at least one number'
    
    if not any(not c.isalnum() for c in password):
        return 'Password must contain at least one special character'

# app.config['MAIL_SERVER']='smtp.gmail.com'
# app.config['MAIL_PORT'] = 465
# app.config['MAIL_USERNAME'] = 'lungcancerprojectde@gmail.com'
# app.config['MAIL_PASSWORD'] = 'vgec@lungcancerde'
# app.config['MAIL_USE_TLS'] = False
# app.config['MAIL_USE_SSL'] = True

# mail = Mail(app)

Session(app)
# mongodb://localhost:27017/lungcancer_db
# mongodb+srv://parth12:EpXlhahdba1O26b8@lungcancerprediction.973sgky.mongodb.net/lungCancerPredictionDB
app.config["MONGO_URI"] = "mongodb://localhost:27017/Brain_Strok_Pridiction"
db = PyMongo(app).db

@app.route('/')
def welcome():
    return render_template('login.html')


@app.route('/login')
def login():
    return render_template('login.html')




@app.route('/signup')
def signup1():
    return render_template('signup.html')

# @app.route("/signup-data", methods=["POST"])
# def signup():
#     name = request.form.get("name")
#     email = request.form.get("email")
#     password = request.form.get("password")
#     # print(pas)
#     conPassword = request.form.get("conPw")
#     if request.method == "POST":
#         # print(db.signup.find({'email':email}))
#         if db.signup.find_one({"email":email}):
#             return render_template('signup.html',data="user is exist")
#         else:
#             if password == conPassword:
#                 db.signup.insert_one({"name":name,"email":email,"password":password,"conform_password":conPassword})
#                 session["name"] = name
#             else:
#                 return render_template('signup.html',pasmsg="password and conform password is not match")
#     return render_template('signup.html')


@app.route('/validate-login', methods=['POST'])
def validate_login():
    email = request.form.get("email")
    password = request.form.get("password")
    encPassword = generate_md5_hash(password)

    userExists = db.signup.find_one({"email":email})

    if request.method == "POST":
        if not email or not password:
            msg = 'Insert credentials properly'
            flash(msg, 'Error')
            return redirect("/login")
        elif not userExists:
            msg = 'No such user exists'
            flash(msg, 'Error')
            return redirect("/login")
        else:
        # if db.signup.find_one({"email":email}):
            userData = db.signup.find_one({"email":email,"password":encPassword})
            # isUserValid = verify_md5_hash(password,encPassword)

            # if isUserValid and userData:
            if userData:
                session["email"] = email
                return render_template("home.html", status = 'Logged in successfully')
            else:
                msg = 'Wrong password... Try again'
                flash(msg, 'Error')
                return redirect("/login")

    # if not password:
    #     msg = 'Password cannot be empty'
    #     flash(msg, 'Error')
    #     return redirect("/login")

# @app.route('/logout')
# def logout():
#     return "Logout"

@app.route('/validate-user', methods=['POST'])
def validate_user():
    import re
    password = request.form.get("password")
    userName = request.form.get("name")
    email = request.form.get("email")
    confirmPassword = request.form.get("confirmPassword")

    date = datetime.now()

    validName = bool(re.match('[a-zA-Z\s]+$', userName))

    if request.method == "POST":
        if not userName or not email or not password or not confirmPassword:
            msg = 'Insert credentials properly'
            flash(msg, 'Error')
            return redirect("/signup")
        
        if not validName:
            msg = 'Name cannot contain numbers or Special characters'
            flash(msg, 'Error')
            return redirect("/signup")
            
        msg = validate_password(password)
        if msg:
            flash(msg, 'Error')
            return redirect("/signup")
                
        if db.signup.find_one({"email":email}):
            msg = 'Email id is alreasy in use'
            flash(msg, 'Error')
            return redirect("/signup")
        else:
            if password == confirmPassword:
                encPassword = generate_md5_hash(password)
                db.signup.insert_one({"name":userName,"email":email,"password":encPassword,"join_timestamp":date})
                session["email"] = email
                return render_template("login.html", status = "Signed up successfully... Please login to continue")
            else:
                msg = 'Password and Confirm password do not match'
                flash(msg, 'Error')
                return redirect("/signup")
                


                
                # return render_template('signup.html',pasmsg="password and conform password is not match")
    # return render_template('signup.html')


    # if not userName or not email or not password:
    #     msg = 'Fill up the credentials properly'
    #     flash(msg, 'Error')
    #     return redirect("/signup")
    

    # if not userName:
    #     msg = 'Name is required'
    #     flash(msg, 'Error')
    #     return redirect("/signup")

    # if not email:
    #     msg = 'Email Id is required'
    #     flash(msg, 'Error')
    #     return redirect("/signup")
    
    # if not password:
    #     msg = 'Password is required'
    #     flash(msg, 'Error')
    #     return redirect("/signup")


    # validateCount = 0
    # msg = ""

    
    # else:
    #     validateCount += 1

    # if password and len(password) < 8:
    #     msg = 'Password must be at least 8 characters long'
    #     flash(msg, 'Error') 
    #     return redirect("/signup")
    # else:
    #     validateCount += 1

    # if password and not any(c.isalnum() for c in password):
        # if msg != " ":
        # msg = 'Password must contain at least one alphanumeric character'
        # flash(msg, 'Error') 
        # return redirect("/signup")
        # else:
        #     msg = 'Password must contain at least one alphanumeric character'
    # else:
    #     validateCount += 1

    # if password and not any(not c.isalnum() for c in password):
    #     # if msg != " ":
    #     msg = 'Password must contain at least one special character'
    #     flash(msg, 'Error') 
    #     return redirect("/signup")
    #     else:
    #         msg = 'Password must contain at least one special character'
    # else:
    #     validateCount += 1

    # if msg != "":
    #     flash(msg, 'Error') 
    #     return redirect("/signup")
    # elif validateCount == 4:
    #     return redirect("/home")


@app.route('/home')
def home():
    if((session["email"])!=False):
        return render_template('home.html')
    else:
          return redirect('/login')
    # return render_template('home.html')

@app.route("/home1")
def index1():
    if not session.get("name"):
        return redirect("/")
    return render_template('home.html')

@app.route('/info')
def info():
    return render_template('info.html')


@app.route('/predict')
def predict():
    return render_template('predict.html')

@app.route('/prediction-data', methods=['POST'])
def predict_data():
    if request.method == "POST":
        name = request.form.get("patient_name")
    
        email = request.form.get("patient_mail")
        age = int(request.form.get("age"))
        import numpy as np
        age = np.sqrt(age)
        from scipy.stats import skew
        skew(age)
        gender = request.form['gender']
        if gender == "Male":
            gender = 1
        else:
            gender = 0

        hypertension = request.form['hyper_tension']
        if hypertension == "Yes":
            hypertension = 1
        else:
            hypertension = 0

        heart_disease = request.form['heart_disease']
        if heart_disease == "Yes":
            heart_disease = 1
        else:
            heart_disease = 0


        ever_married = request.form['ever_married']
        if ever_married == "Yes":
            ever_married = 1
        else:
            ever_married = 0


        # work_type = request.form['work_type']
        # if work_type == "private":
        #     work_type = 2
        # elif work_type == "self-employed":
        #     work_type = 3
        # elif work_type == "Govt_job":
        #     work_type = 0
        # elif work_type == "children":
        #     work_type = 4
        # elif work_type == "never_worked":
        #     work_type = 1
            


        Residence_type = request.form['residence_type']
        if Residence_type == "Urban":
            Residence_type = 1
        else:
            Residence_type = 0



        avg_glucose_level = float(request.form['avg_glucose_level'])
       

        bmi = float(request.form['bmi'])
       
        smoking_status_mapping = {"formerly_smoked": 1, "never_smoked": 2, "smoked": 3}
        smoking_status = smoking_status_mapping.get(request.form['smoke'], 0)
        print(smoking_status)

        li = [gender,age,hypertension,heart_disease,ever_married,Residence_type,avg_glucose_level,bmi,smoking_status]
        # n = []
        import numpy as np

        # import xgboost as xgb


        from datetime import datetime

        date = datetime.now()
        print("li",li)
        temp = loaded_model2.transform(np.array(li).reshape(1, -1))
        print("tem",temp)
        result = int(loaded_model.predict(temp)[0])
        print("re",result)
        db.brain_stroke_predict_info.insert_one({"name":name,"email":email,"age":age,"gender":gender,"hypertension":hypertension,"heart_disease":heart_disease,"ever_married":ever_married,"Residence_type":Residence_type,"avg_glucose_level":avg_glucose_level,"bmi":bmi,"smoking_status":smoking_status,"date":date,"result":result})
        
        if(int(loaded_model.predict(temp.reshape(1,-1))[0])==0):
            return render_template("predict.html", data1="PATIENT MAY NOT HAVE BRAIN STROKE")
        else:
            return render_template("predict.html", data2="PATIENT MAY HAVE BRAIN STROKE")



@app.route('/about')
def about():
    # return render_template('about.html')
    return "About"


@app.route('/contact')
def contact():
    return render_template('contact.html')

# @app.route('/go-reconfirm-password')
# def go_reconfirm_password():
#     # msg = validate_password(password)
#     # if msg:
#         # flash(msg, 'Error')
#     return redirect("/go-reconfirm-password")
    
@app.route('/reconfirm-password', methods=['POST'])
def re_confirm_password():
    password = request.form.get('password')
    confirmPassword = request.form.get('confirmPassword')
    email = request.form.get('email')
    
    if not password or not confirmPassword:
        msg = 'Insert both password fields'
        flash(msg, 'Error')
        return render_template('reconfirm_password.html', email = email)

    if password == confirmPassword:
        encPassword = generate_md5_hash(password)
        msg = validate_password(password)
        date = datetime.now()
        if msg:
            flash(msg, 'Error')
            return render_template('reconfirm_password.html', email = email)
        else:
            db.signup.update_one({"email":email}, {"$set": {"password":encPassword, "password_reset_timestamp": date}})
            return render_template('login.html', status = 'Password reset successfully')
        
    else:
        msg = 'Password and Confirm Password do not match'
        flash(msg, 'Error')
        return render_template('reconfirm_password.html', email = email)

@app.route("/logout")
def logout():
    session["email"] = False
    return redirect("/login")

@app.route("/reset-password")
def reset_password():
    return render_template("reset_password.html")

@app.route("/validate-reset-password", methods=['POST'])
def validate_reset_password():
    i1 = request.form.get("otp1")
    i2 = request.form.get("otp2")
    i3 = request.form.get("otp3")
    i4 = request.form.get("otp4")
    i5 = request.form.get("otp5")
    i6 = request.form.get("otp6")
    email = request.form.get("email")
    actualOtp = request.form.get("hiddenOtp")
    otpVal = i1 + i2 + i3 + i4 + i5 + i6

    result = verify_md5_hash(otpVal, actualOtp)
    if result:
        return render_template("reconfirm_password.html", email = email)
    else:
        msg = 'Wrong OTP inserted'
        flash(msg,"Error")
        return render_template('reset_password.html', email = email, encOtp = actualOtp)
        
    # return f"Inserted OTP value is {otpVal}, Actual OTP encryption was {actualOtp}, and the match is {result}"

@app.route("/send-otp", methods=["POST"])
def send_otp():   
    dest_mail = request.form.get("email")
    userExists = db.signup.find_one({"email":dest_mail})

    if userExists:
        import smtplib
        import random

        my_mail = "lungcancerprojectde@gmail.com"
        passcode = "suqvifhxeffhutdm"

        connection = smtplib.SMTP("smtp.gmail.com", 587)
        connection.starttls()
        connection.login(user=my_mail, password=passcode)

        otp = str(random.randint(100000,999999))

        encOtp = generate_md5_hash(otp)

        subject = "OTP for Reset Password"
        msg = f"Dear User,\n\nIt appears that you have requested a password reset for your account. To ensure the security of your account, we are happy to assist you with this process.\n\nYou will require OTP: {otp} to reset your password\n\nThank You,\nRegards\n\nNote: Kindly do not reply for this mail"

        mail_content = f"Subject: {subject} \n\n {msg}"

        try:
            connection.sendmail(from_addr=my_mail, to_addrs=dest_mail, msg=mail_content)
            return render_template("reset_password.html", status="OTP sent successfully", email=dest_mail, encOtp = encOtp)
        except Exception as e:
            return "Something went wrong while sending the mail"
        finally:
            connection.close()
    else:
        msg = 'No such user exists'
        flash(msg,'Error')
        return render_template("reset_password.html")
    
@app.route('/contact-us', methods=['POST'])
def contactUs():
    import smtplib

    my_mail = "lungcancerprojectde@gmail.com"
    passcode = "suqvifhxeffhutdm"

    connection = smtplib.SMTP("smtp.gmail.com", 587)
    connection.starttls()
    connection.login(user=my_mail, password=passcode)

    name = request.form.get('name')
    mail = request.form.get('mail')
    message = request.form.get('message')

    subject = f"Contact Message from {name}"
    msg = f"Name: {name}\n Message: {message}"

    mail_content = f"Subject: {subject} \n\n {msg}"

    try:
        connection.sendmail(from_addr=mail, to_addrs=my_mail, msg=mail_content)
        return render_template("contact.html", status="Message sent successfully")
    except Exception as e:
        return "Something went wrong"
    finally:
        connection.close()

if __name__ == '__main__':
    app.run(debug=True)




# @app.route('/login-data', methods=["POST"])
# def login1():
#     email = request.form.get("email")
#     pas = request.form.get("pas")
#     if request.method == "POST":
#         if db.signup.find_one({"email":email,"password":pas}):
#             session["email"] = request.form.get("email")
#             return render_template("home.html")
#         else:
#             return render_template("login.html",invalid_uname="wrong id & password")
#     return redirect("/login")