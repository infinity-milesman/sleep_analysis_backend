from flask import Flask

from flask_sqlalchemy import SQLAlchemy
from flask import Flask, jsonify, request
from flask_migrate import Migrate
from sqlalchemy import desc




app = Flask(__name__)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from flask_sqlalchemy import SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:@localhost/sleep_analysis_backend'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

from models import  *

@app.route('/')
def hello():
    return "Hello World!"

@app.route('/register',methods=['POST','OPTIONS'])
def register():
    data = request.get_json()
    mobile = data.get('mobile',None) #Send the status as 'D' by defualt and activate after user_verify
    email = data.get('email', None)
    print(data)
    if email is None or mobile is None:
        return jsonify({"status":0,"data":"email or mobile number is not present in the request"}),401
    check_mobile_exist = db.session.query(User).filter(User.mobile == mobile).first()
    if check_mobile_exist:
        return jsonify({"status": 0, "data": "Mobile number is already registered with us"}), 401
    check_email_exist = db.session.query(User).filter(User.email == email).first()
    if check_email_exist:
        return jsonify({"status": 0, "data": "Email is already registered with us"}), 401
    user_data = User(**data)
    # otp = generate_otp()
    # print(otp)
    # insert_into_user_veriry(mobile,otp,'A')
    # message = '{0} is your OTP.Please use it for verification'.format(otp)
    # try:
    #     sendSms(mobile, message)
    # except Exception as e:
    #     print("Unable to send sms")
    #     print(e)

    print(user_data)
    db.session.add(user_data)
    db.session.commit()
    return jsonify({"status":1,"user_id":user_data.id}),200



@app.route("/login",methods = ['POST','OPTIONS'])
def home():
    email = request.values.get('email')
    password = request.values.get('password')
    mobile = request.values.get('mobile')
    if not email and not mobile:
        return jsonify({"status": 0, "data": "please provide email id or mobile"}), 401
    if not password:
        return jsonify({"status": 0, "data": "please provide password"}), 401
    if email:
        check_email_exist = db.session.query(User).filter(User.email == email).first()
        if not check_email_exist:
            return jsonify({"status": 0, "data": "incorrect email"}), 401
        db_password = db.session.query(User).filter(User.email == email).first()
        if db_password.password != password:
            return jsonify({"status": 0, "data": "incorrect password "}), 401

    # if mobile:
    #     check_mobile_exist = db.session.query(User).filter(User.mobile == mobile).first()
    #     if not check_mobile_exist:
    #         return jsonify({"status": 0, "data": "incorrect mobile"}), 401
    #     db_password = db.session.query(User).filter(User.mobile == mobile).first()
    #     if db_password.password != password:
    #         return jsonify({"status": 0, "data": "incorrect password "}), 401

    return jsonify({"status": 1, "user_id": db_password.id}),200




if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port='8089')