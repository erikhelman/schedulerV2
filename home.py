from flask import Flask, jsonify, render_template, request, url_for, redirect, json
from security import pwd_context
import uuid
from send_email import send_mail
import jwt
from flask_sqlalchemy import SQLAlchemy
import os
from flask_cors import CORS
import string
import random
from time import time
import arrow

app = Flask(__name__)

app.config.from_pyfile('config.py')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']

CORS(app, resources={r"https://floating-fortress-53646.herokuapp.com/*": {"origins": "*"}, r"/*": {"supports_credentials": True}})

db = SQLAlchemy(app)
url = "https://glacial-sierra-90432.herokuapp.com/"


class Users(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(100))
    status = db.Column(db.String(10)) # active, inactive, pending
    role = db.Column(db.String(5))
    email = db.Column(db.String(50))
    students = db.relationship('Students', backref='login', lazy='dynamic')
    info = db.relationship('Profile', backref='users', uselist=False)


class Students(db.Model):
    student_id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(25))
    lname = db.Column(db.String(25))
    gender = db.Column(db.String(1))
    dob = db.Column(db.DateTime(timezone=True))
    level = db.Column(db.Integer)
    class_type = db.Column(db.String(30))
    class_length = db.Column(db.Integer)
    status = db.Column(db.String(20)) # values = Active, Inactive
    emerg_contact = db.Column(db.String(50))
    emerg_phone = db.Column(db.String(20))
    previous_school = db.Column(db.String(100))
    pref_day0 = db.Column(db.String(9))
    pref_start_time0 = db.Column(db.DateTime(timezone=True))
    pref_end_time0 = db.Column(db.DateTime(timezone=True))
    pref_day1 = db.Column(db.String(9))
    pref_start_time1 = db.Column(db.DateTime(timezone=True))
    pref_end_time1 = db.Column(db.DateTime(timezone=True))
    pref_day2 = db.Column(db.String(9))
    pref_start_time2 = db.Column(db.DateTime(timezone=True))
    pref_end_time2 = db.Column(db.DateTime(timezone=True))
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    classes = db.relationship('Classes', backref='students', lazy='dynamic')
    payments = db.relationship('Payments', backref='students', lazy='dynamic')


class Profile(db.Model):
    info_id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(50))
    lname = db.Column(db.String(50))
    customer_id = db.Column(db.Integer)
    city = db.Column(db.String(50))
    province = db.Column(db.String(2))
    street = db.Column(db.String(200))
    postal = db.Column(db.String(6))
    phone = db.Column(db.String(10))
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))


class Config(db.Model):
    config_id = db.Column(db.Integer, primary_key=True)
    reschedules_allowed = db.Column(db.Integer)
    notice_required = db.Column(db.Integer)


class Session(db.Model):
    session_id = db.Column(db.Integer, primary_key=True)
    start_date = db.Column(db.DateTime(timezone=True))
    end_date = db.Column(db.DateTime(timezone=True))
    current_session = db.Column(db.Boolean)
    next_session = db.Column(db.Boolean)
    class_id = db.relationship('Classes', backref='session', lazy='dynamic')
    payment_id = db.relationship('Payments', backref='payments', lazy='dynamic')
    #session_schedule = db.relationship('Schedules', backref='session', lazy='dynamic')


class Classes(db.Model):
    class_id = db.Column(db.Integer, primary_key=True)
    class_start = db.Column(db.DateTime(timezone=True))
    class_end = db.Column(db.DateTime(timezone=True))
    student_id = db.Column(db.Integer, db.ForeignKey('students.student_id'))
    session_id = db.Column(db.Integer, db.ForeignKey('session.session_id'))


class Payments(db.Model):
    payment_id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.student_id'))
    session_id = db.Column(db.Integer, db.ForeignKey('session.session_id'))
    price = db.Column(db.Integer)
    paid = db.Column(db.Boolean)


class Locations(db.Model):
    location_id = db.Column(db.Integer, primary_key=True)
    location_name = db.Column(db.String(50))
    lanes = db.Column(db.Integer)
    loc_schedule = db.relationship('Schedules', backref='locations', lazy='dynamic')


class Schedules(db.Model):
    schedule_id = db.Column(db.Integer, primary_key=True)
    schedule_name = db.Column(db.String(25))
    #session_id = db.Column(db.Integer, db.ForeignKey('session.session_id'))
    location_id = db.Column(db.Integer, db.ForeignKey('locations.location_id'))
    definitions = db.relationship('ScheduleDefinitions', backref='schedule', lazy='dynamic')


class ScheduleDefinitions(db.Model):
    schedule_def_id = db.Column(db.Integer, primary_key=True)
    lane = db.Column(db.String(10))
    max_students = db.Column(db.Integer)
    min_level = db.Column(db.Integer)
    max_level = db.Column(db.Integer)
    class_type_id = db.Column(db.Integer, db.ForeignKey('class_types.class_type_id'))
    class_type = db.relationship('ClassTypes', foreign_keys=[class_type_id])
    class_length_id = db.Column(db.Integer, db.ForeignKey('prices.price_id'))
    class_length = db.relationship('Prices', foreign_keys=[class_length_id])
    class_start = db.Column(db.Time(timezone=True))
    class_end = db.Column(db.Time(timezone=True))
    split_lane = db.Column(db.Boolean)
    spots_left = db.Column(db.Integer)
    schedule_id = db.Column(db.Integer, db.ForeignKey('schedules.schedule_id'))


class Instructors(db.Model):
    instructor_id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(50))
    lname = db.Column(db.String(50))
    phone = db.Column(db.String(10))
    email = db.Column(db.String(50))


class ClassTypes(db.Model):
    class_type_id = db.Column(db.Integer, primary_key=True)
    class_type = db.Column(db.String(30))
    num_students = db.Column(db.Integer)


class Prices(db.Model):
    price_id = db.Column(db.Integer, primary_key=True)
    class_length = db.Column(db.Integer)
    price = db.Column(db.Integer)


def authenticate(token):

    try:
        payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms='HS256')

    except jwt.ExpiredSignatureError:
        return False, "Token has expired, please log in again"

    except (jwt.DecodeError, jwt.InvalidTokenError):
        return False, "Invalid token provided"

    else:
        return True, payload

@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':

        data = json.loads(request.data.decode('utf8'))
        email = data['email'].lower()
        password = data['password']

        user = Users.query.filter(Users.email == email).first()

        if user:

            if user.status == 'active':

                if pwd_context.verify(password,user.password):

                    payload = {'user_id' : user.public_id}
                    token = (jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256').decode("utf-8"))
                    return jsonify({"isAuthenticated": "true", "role": user.role, "token": token})

                return jsonify({"isAuthenticated": "false", "error": "Email address and/or password are incorrect."})

            elif user.status == 'inactive':

                return jsonify({"isAuthenticated": "false",
                                "error": "This account has been deactivated. Please contact the administrator for more details."})

            elif user.status == 'pending':

                return jsonify({"isAuthenticated": "false",
                                "error": "This account has not yet been activated. Once registration has been completed, you will be contacted with further details."})

        return jsonify({"isAuthenticated": "false", "error": "Username and/or password are incorrect."})

    return ''


@app.route('/register', methods=['POST'])
def register():
    if request.method == 'POST':
        payload = request.data.decode('utf8')
        data = json.loads(payload)

        with open ('testfile.txt','w') as f:
            json.dump(data, f)

        email = data['email'].lower().strip()
        password = data['password']

        if Users.query.filter(Users.email == email).first() is None:

            user = Users(public_id=uuid.uuid4(),
                         password=pwd_context.hash(password),
                         status='pending',
                         role='user',
                         email=email)

            user.info = Profile(fname=data['fname'],
                                lname=data['lname'],
                                customer_id=None,
                                city=None,
                                province=None,
                                street=None,
                                postal=None,
                                phone=data['phone'])

            for s in data['students']:

                with open('student.txt', 'w') as f:
                    json.dump(s, f)

                new_student = Students(fname=s['fname'],
                                       lname=s['lname'],
                                       gender=s['gender'],
                                       dob=s['pDOB'],
                                       level=s['level'],
                                       class_type=s['classType'],
                                       class_length=s['classLength'],
                                       status='Pending',
                                       emerg_contact=s['emergName'],
                                       emerg_phone=s['emergContact'],
                                       previous_school=s['previousSchool'],
                                       pref_day0=s['prefDay'][0],
                                       pref_start_time0=s['pStartTime'][0] if s['pStartTime'][0] !='' else None,
                                       pref_end_time0=s['pEndTime'][0] if s['pEndTime'][0] !='' else None,
                                       pref_day1=s['prefDay'][1],
                                       pref_start_time1=s['pStartTime'][1] if s['pStartTime'][1] !='' else None,
                                       pref_end_time1=s['pEndTime'][1] if s['pEndTime'][1] !='' else None,
                                       pref_day2=s['prefDay'][2],
                                       pref_start_time2=s['pStartTime'][2] if s['pStartTime'][2] !='' else None,
                                       pref_end_time2=s['pEndTime'][2] if s['pEndTime'][2] !='' else None
                                       )

                user.students.append(new_student)

            db.session.add(user)
            db.session.commit()

            send_mail(
                'helman.erik@gmail.com',
                'Registration - Action Required',
                'A new user has registered in the system, ' + data['fname'] + ' ' + data['lname']+ '.'

            )

            return jsonify({"isRegistered": "true"})

        else:
            return jsonify({"isRegistered": "false",
                            "errors": "This email address is already registered in the system. If you have forgotten your password, please click the password recovery link."})

    return ''


@app.route('/profile', methods=['POST'])
def get_profile():

    if request.method == 'POST':
        payload = request.data.decode('utf8')
        data = json.loads(payload)

        result, tokenData = authenticate(data['token'])

        if result:

            user_id = tokenData['user_id']
            profile = Users.query.filter(Users.public_id == user_id).first()

            user_profile = {}
            user_profile['fname'] = profile.info.fname
            user_profile['lname'] = profile.info.lname
            user_profile['city'] = profile.info.city
            user_profile['province'] = profile.info.province
            user_profile['street'] = profile.info.street
            user_profile['postal'] = profile.info.postal
            user_profile['phone'] = profile.info.phone
            user_profile['email'] = profile.email

            return jsonify(user_profile)

        else:

            return {"error": tokenData}

    return ''


@app.route('/update_profile', methods=['POST'])
def update_profile():
    if request.method == 'POST':
        payload = request.data.decode('utf8')
        data = json.loads(payload)

        with open ('testfile.txt','w') as f:
           json.dump(data, f)

        try:
            token = jwt.decode(data['token'], app.config['SECRET_KEY'], algorithms='HS256')

        except jwt.ExpiredSignatureError:
            return "Token has expired, please log in again"

        except (jwt.DecodeError, jwt.InvalidTokenError):
            return "Invalid token provided"

        else:
            user_id = token['user_id']
            user = Users.query.filter(Users.public_id == user_id).first()

            if data['phone'] == '':
                data['phone'] = None

            user.info.fname = data['fname']
            user.info.lname = data['lname']
            user.info.city = data['city']
            user.info.province = data['province']
            user.info.street = data['street']
            user.info.postal = data['postal']
            user.info.phone = data['phone']
            user.email = data['email']

            db.session.add(user)
            db.session.commit()

            return jsonify({"profileUpdate": "true"})

    return ''


@app.route('/students', methods=['POST'])
def get_students():
    if request.method == 'POST':
        payload = request.data.decode('utf8')
        data = json.loads(payload)

        try:
            token = jwt.decode(data['token'], app.config['SECRET_KEY'], algorithms='HS256')

        except jwt.ExpiredSignatureError:
            return "Token has expired, please log in again"

        except (jwt.DecodeError, jwt.InvalidTokenError):
            return "Invalid token provided"

        else:
            user_id = token['user_id']
            user = Users.query.filter(Users.public_id == user_id).first()

            userdata = {}
            userdata['students'] = []

            for s in user.students:

                new_student = {'student_id': s.student_id,
                               'fname': s.fname if s.fname != None else '',
                               'lname': s.lname if s.lname != None else '',
                               'dob': s.dob.isoformat() if s.dob != None else s.dob,
                               'gender': s.gender if s.gender != None else '',
                               'level': s.level if s.level != None else '',
                               'class_type': s.class_type if s.gender != None else '',
                               'class_length': s.class_length if s.class_length != None else '',
                               'status': s.status if s.status != None else '',
                               'emerg_contact': s.emerg_contact if s.emerg_contact != None else '',
                               'emerg_phone': s.emerg_phone if s.emerg_phone != None else ''}

                userdata['students'].append(new_student)

            return jsonify(userdata)

    return ''


@app.route('/update_students', methods=['POST'])
def update_students():
    if request.method == 'POST':
        payload = request.data.decode('utf8')
        data = json.loads(payload)

        with open ('testfile.txt','w') as f:
            json.dump(data, f)

        try:
            token = jwt.decode(data['token'], app.config['SECRET_KEY'], algorithms='HS256')

        except jwt.ExpiredSignatureError:
            return "Token has expired, please log in again"

        except (jwt.DecodeError, jwt.InvalidTokenError):
            return "Invalid token provided"

        else:
            user_id = token['user_id']
            user = Users.query.filter(Users.public_id == user_id).first()

            if user.students.count() != len(data['students']):

                for es in user.students:

                    match = False

                    for ds in data['students']:

                        if es.student_id == ds['student_id']:

                            match = True

                    if not match:

                        Students.query.filter(Students.student_id==es.student_id).delete()

            for s in data['students']:

                date = None
                class_length = None
                emerg_phone = None

                if 'dob' in s:

                    if s['dob'] != '':
                        date = s['dob']

                if 'class_length' in s:

                    if s['class_length'] != '':

                        class_length = s['class_length']

                if 'emerg_phone' in s:

                    if s['emerg_phone'] != '':

                        emerg_phone = s['emerg_phone']

                if s['student_id'] == str(-1):

                    new_student = Students(fname = s['fname'] if 'fname' in s else None,
                                           lname=s['lname'] if 'lname' in s else None,
                                           gender=s['gender'] if 'gender' in s else None,
                                           dob = date,
                                           level=s['level'] if 'level' in s else None,
                                           class_type=s['class_type'] if 'class_type' in s else None,
                                           class_length= class_length,
                                           emerg_contact=s['emerg_contact'] if 'emerg_contact' in s else None,
                                           emerg_phone=emerg_phone)

                    user.students.append(new_student)

                else:

                    for es in user.students:

                        if es.student_id == s['student_id']:
                            es.fname = s['fname'] if 'fname' in s else None
                            es.lname = s['lname'] if 'lname' in s else None
                            es.gender = s['gender'] if 'gender' in s else None
                            es.dob = date
                            es.level = s['level'] if 'level' in s else None
                            es.class_type = s['class_type'] if 'class_type' in s else None
                            es.class_length = class_length
                            es.emerg_contact=s['emerg_contact'] if 'emerg_contact' in s else None
                            es.emerg_phone=emerg_phone

            db.session.add(user)
            db.session.commit()

            userdata = {}
            userdata['students'] = []

            for s in user.students:
                new_student = {'student_id': s.student_id,
                               'fname': s.fname if s.fname != None else '',
                               'lname': s.lname if s.lname != None else '',
                               'dob': s.dob.isoformat() if s.dob != None else s.dob,
                               'gender': s.gender if s.gender != None else '',
                               'level': s.level if s.level != None else '',
                               'class_type': s.class_type if s.gender != None else '',
                               'class_length': s.class_length if s.class_length != None else '',
                               'status': s.status if s.status != None else '',
                               'emerg_contact': s.emerg_contact if s.emerg_contact != None else '',
                               'emerg_phone': s.emerg_phone if s.emerg_phone != None else ''}

                userdata['students'].append(new_student)

            userdata['studentUpdate'] = True

            return jsonify(userdata)

    return ''


@app.route('/update_admin_student', methods=['POST'])
def update_admin_student():
    if request.method == 'POST':
        payload = request.data.decode('utf8')
        data = json.loads(payload)

        with open ('testfile.txt','w') as f:
            json.dump(data, f)


        try:
            token = jwt.decode(data['token'], app.config['SECRET_KEY'], algorithms='HS256')

        except jwt.ExpiredSignatureError:
            return "Token has expired, please log in again"

        except (jwt.DecodeError, jwt.InvalidTokenError):
            return "Invalid token provided"

        else:
            student_id = data['id']
            s = Students.query.filter(Students.student_id == student_id).first()

            date = None
            class_length = None
            emerg_phone = None

            if 'dob' in s:

                if s['dob'] != '':
                    date = s['dob']

            if data['class_length'] != '':

                class_length = data['class_length']

            if data['emerg_phone'] != '':

                emerg_phone = data['emerg_phone']

            s.fname = data['fname'] if data['fname'] != '' else None
            s.lname = data['lname'] if data['lname'] != '' else None
            s.gender = data['gender'] if data['gender'] != '' else None
            s.dob = date
            s.level = data['level'] if data['level'] != '' else None
            s.class_type = data['class_type'] if data['class_type'] != '' else None
            s.class_length = class_length
            s.emerg_contact=data['emerg_contact'] if data['emerg_phone'] != '' else None
            s.emerg_phone=emerg_phone

            db.session.add(s)
            db.session.commit()

            return jsonify({"studentUpdate": "true"})

    return ''


@app.route('/admin_student', methods=['POST'])
def get_admin_student():
    if request.method == 'POST':
        payload = request.data.decode('utf8')
        data = json.loads(payload)

        with open ('testfile.txt','w') as f:
            json.dump(data, f)

        try:
            token = jwt.decode(data['token'], app.config['SECRET_KEY'], algorithms='HS256')

        except jwt.ExpiredSignatureError:
            return "Token has expired, please log in again"

        except (jwt.DecodeError, jwt.InvalidTokenError):
            return "Invalid token provided"

        else:
            student_id = data['id']
            s = Students.query.filter(Students.student_id == student_id).first()

            userdata = {'student_id': s.student_id,
                           'fname': s.fname if s.fname != None else '',
                           'lname': s.lname if s.lname != None else '',
                           'dob': s.dob.isoformat() if s.dob != None else s.dob,
                           'gender': s.gender if s.gender != None else '',
                           'level': s.level if s.level != None else '',
                           'class_type': s.class_type if s.gender != None else '',
                           'class_length': s.class_length if s.class_length != None else '',
                           'status': s.status if s.status != None else '',
                           'emerg_contact': s.emerg_contact if s.emerg_contact != None else '',
                           'emerg_phone': s.emerg_phone if s.emerg_phone != None else ''}

            return jsonify(userdata)

    return ''


@app.route('/all_students', methods=['POST'])
def get_all_students():
    if request.method == 'POST':

        payload = request.data.decode('utf8')
        data = json.loads(payload)

        try:
            jwt.decode(data['token'], app.config['SECRET_KEY'], algorithms='HS256')

        except jwt.ExpiredSignatureError:
            return "Token has expired, please log in again"

        except (jwt.DecodeError, jwt.InvalidTokenError):
            return "Invalid token provided"

        else:

            all_students = Students.query.order_by(Students.student_id).all()
            current_session_id = Session.query.filter(Session.current_session == True).first()
            next_session_id = Session.query.filter(Session.next_session == True).first()
            current_session_paid = None
            next_session_paid = None

            userdata = {}
            userdata['students'] = []

            for s in all_students:

                for p in s.payments:

                    if p.session_id == current_session_id.session_id:

                        if p.paid:
                            current_session_paid = 'Yes'
                        else:
                            current_session_paid = 'No'

                    elif p.session_id == next_session_id.session_id:

                        if p.paid:
                            next_session_paid = 'Yes'
                        else:
                            next_session_paid = 'No'

                new_student = {'student_id': s.student_id,
                               'fname': s.fname,
                               'lname': s.lname,
                               'dob': s.dob,
                               'gender': s.gender,
                               'level': s.level,
                               'class_type': s.class_type,
                               'class_length': s.class_length,
                               'status': s.status,
                               'emerg_contact': s.emerg_contact,
                               'emerg_phone': s.emerg_phone,
                               'previous_school': s.previous_school,
                               'pref_day0': s.pref_day0,
                               'pref_start_time0': s.pref_start_time0,
                               'pref_end_time0': s.pref_end_time0,
                               'pref_day1': s.pref_day1,
                               'pref_start_time1': s.pref_start_time1,
                               'pref_end_time1': s.pref_end_time1,
                               'pref_day2': s.pref_day2,
                               'pref_start_time2': s.pref_start_time2,
                               'pref_end_time2': s.pref_end_time2,
                               'current_session_paid': current_session_paid,
                               'next_session_paid': next_session_paid
                               }

                userdata['students'].append(new_student)

            return jsonify(userdata)


@app.route('/all_users', methods=['POST'])
def get_all_users():
    if request.method == 'POST':



        payload = request.data.decode('utf8')
        data = json.loads(payload)

        try:
            jwt.decode(data['token'], app.config['SECRET_KEY'], algorithms='HS256')

        except jwt.ExpiredSignatureError:
            return "Token has expired, please log in again"

        except (jwt.DecodeError, jwt.InvalidTokenError):
            return "Invalid token provided"

        else:

            all_users = Users.query.order_by(Users.user_id).all()
            userdata = {}
            userdata['users'] = []
            for u in all_users:

                new_user = {'id': u.public_id,
                            'status': u.status,
                            'email': u.email,
                            'role': u.role,
                            'fname': u.info.fname,
                            'lname': u.info.lname,
                            'customerID': u.info.customer_id,
                            'city': u.info.city,
                            'province': u.info.province,
                            'street': u.info.street,
                            'postal': u.info.postal,
                            'phone': u.info.phone}

                userdata['users'].append(new_user)

        return jsonify(userdata)

    return ''


@app.route('/admin_user', methods=['POST'])
def get_admin_user():
    if request.method == 'POST':
        payload = request.data.decode('utf8')
        data = json.loads(payload)

        with open ('testfile.txt','w') as f:
            json.dump(data, f)


        try:
            token = jwt.decode(data['token'], app.config['SECRET_KEY'], algorithms='HS256')

        except jwt.ExpiredSignatureError:
            return "Token has expired, please log in again"

        except (jwt.DecodeError, jwt.InvalidTokenError):
            return "Invalid token provided"

        else:
            user_id = data['id']
            u = Users.query.filter(Users.public_id == user_id).first()


            userdata = {'id': u.public_id,
                        'status': u.status,
                        'role': u.role,
                        'fname': u.info.fname if u.info.fname != None else '',
                        'lname': u.info.lname if u.info.lname != None else '',
                        'email': u.email,
                        'customerID': u.info.customer_id if u.info.customer_id != None else '',
                        'phone': u.info.phone if u.info.phone != None else '',
                        'city': u.info.city if u.info.city != None else '',
                        'province': u.info.province if u.info.province != None else '',
                        'street': u.info.street if u.info.street != None else '',
                        'postal': u.info.postal if u.info.postal != None else ''}

            return jsonify(userdata)

    return ''


@app.route('/update_admin_user', methods=['POST'])
def update_admin_user():
    if request.method == 'POST':
        payload = request.data.decode('utf8')
        data = json.loads(payload)

        with open ('testfile.txt','w') as f:
            json.dump(data, f)

        try:
            token = jwt.decode(data['token'], app.config['SECRET_KEY'], algorithms='HS256')

        except jwt.ExpiredSignatureError:
            return "Token has expired, please log in again"

        except (jwt.DecodeError, jwt.InvalidTokenError):
            return "Invalid token provided"

        else:
            user_id = data['id']
            u = Users.query.filter(Users.public_id == user_id).first()

            phone = None

            if data['phone'] != '':

                phone = data['phone']

            u.info.fname = data['fname']
            u.info.lname = data['lname']
            u.role = data['role'] if data['role'] != '' else None
            u.status = data['status']
            u.info.customer_id = data['customerID'] if 'customerID' in 'data' and data['customerID'] !='' else None
            u.city = data['city'] if 'city' in  data else ''
            u.info.province = data['province'] if 'province' in data else ''
            u.info.street=data['street'] if 'street' in data else ''
            u.info.postal=data['postal'] if 'postal' in data else ''
            u.info.phone=phone
            u.email = data['email']

            db.session.add(u)
            db.session.commit()

            return jsonify({"userUpdate": "true"})

    return ''


@app.route('/instructors', methods=['POST'])
def get_instructors():
    if request.method == 'POST':

        payload = request.data.decode('utf8')
        data = json.loads(payload)

        try:
            jwt.decode(data['token'], app.config['SECRET_KEY'], algorithms='HS256')

        except jwt.ExpiredSignatureError:
            return "Token has expired, please log in again"

        except (jwt.DecodeError, jwt.InvalidTokenError):
            return "Invalid token provided"

        else:

            all_instructors = Users.query.filter(Users.role=='inst').order_by(Users.user_id).all()
            userdata = {}
            userdata['instructors'] = []

            for i in all_instructors:

                new_instructor = {'id': i.public_id,
                                  'username': i.username,
                                  'email': i.email,
                                  'status': i.status,
                                  'fname': i.info.fname,
                                  'lname': i.info.lname,
                                  'phone': i.info.phone}

                userdata['instructors'].append(new_instructor)

            return jsonify(userdata)


@app.route('/add_instructor', methods=['POST'])
def add_instructor():
    if request.method == 'POST':
        payload = request.data.decode('utf8')
        data = json.loads(payload)
        username = data['username'].lower().strip()

        try:
            token = jwt.decode(data['token'], app.config['SECRET_KEY'], algorithms='HS256')

        except jwt.ExpiredSignatureError:
            return "Token has expired, please log in again"

        except (jwt.DecodeError, jwt.InvalidTokenError):
            return "Invalid token provided"

        else:

            if data['phone'] == '':
                data['phone'] = None

            if Users.query.filter(Users.username == data['username']).first() is None:
                password = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(10))

                instructor_profile = Profile(fname = data['fname'],
                                             lname = data['lname'],
                                             customer_id = None,
                                             city = None,
                                             province = None,
                                             street = None,
                                             postal = None,
                                             phone = data['phone'])

                instructor = Users(public_id=uuid.uuid4(),
                                   username=username,
                                   password=pwd_context.hash(password),
                                   status='active',
                                   role='inst',
                                   email=data['email'],
                                   info=instructor_profile)

                db.session.add(instructor)
                db.session.commit()

                all_instructors=Users.query.filter(Users.role=='inst').order_by(Users.user_id).all()
                userdata = {}
                userdata['instructors'] = []
                for i in all_instructors:
                    new_instructor = {'id': i.public_id,
                                'username': i.username,
                                'status': i.status,
                                'email': i.email,
                                'fname': i.info.fname,
                                'lname': i.info.lname,
                                'phone': i.info.phone}

                    userdata['instructors'].append(new_instructor)

                userdata['isRegistered'] = True

                return jsonify(userdata)

            else:
                return jsonify({"isRegistered": "false",
                                "errors": "This user name already exists, please select a different one."})

    return ''


@app.route('/recovery', methods=['POST'])
def password_recovery():
    if request.method == 'POST':
        payload = request.data.decode('utf8')
        data = json.loads(payload)

        email = data['email'].lower()
        expiry = 3600

        with open ('testfile.txt','w') as f:
            json.dump(data, f)

        user = Users.query.filter(Users.email == email).first()

        if user:

            token_data = {'user_id': user.public_id, 'exp': time() + expiry}
            token = (jwt.encode(token_data, app.config['SECRET_KEY'], algorithm='HS256').decode("utf-8"))

            reset_url = 'http://localhost:5000/password_reset/' + token

            send_mail(email, 'Password Reset Request', 'This is a password reset request. Click the link below \n' + reset_url)

        return jsonify({"recoverySuccessful": "true"})

    return jsonify({"recoverySuccessful": "false"})


@app.route('/password_reset/<token>', methods=['GET', 'POST'])
def password_reset(token):
    if request.method == 'GET':

        return ''

    return ''


@app.route('/get_config', methods=['GET'])
def get_config():
    if request.method == 'GET':

        userdata={}

        config_data = Config.query.first()


        current_session = Session.query.filter(Session.current_session == True).first()
        next_session = Session.query.filter(Session.next_session == True).first()

        if config_data is None:
            userdata['notice'] = ''
            userdata['numberAllowed'] = ''

        else:

            userdata['notice'] = config_data.notice_required
            userdata['numberAllowed'] = config_data.reschedules_allowed

        if current_session is None:

            userdata['current_start_date'] = ''
            userdata['current_end_date'] = ''

        else:

            userdata['current_start_date'] = current_session.start_date.isoformat()
            userdata['current_end_date'] = current_session.end_date.isoformat()

        if next_session is None:

            userdata['next_start_date'] = ''
            userdata['next_end_date'] = ''

        else:

            userdata['next_start_date'] = next_session.start_date.isoformat()
            userdata['next_end_date'] = next_session.end_date.isoformat()

        class_types = ClassTypes.query.all()
        userdata['existing_classes'] = []

        for ct in class_types:

            new_type = {'class_type_id': ct.class_type_id,
                        'class_type': ct.class_type,
                        'num_students': ct.num_students}

            userdata['existing_classes'].append(new_type)

        prices = Prices.query.all()
        userdata['existing_prices'] = []

        for p in prices:

            new_price = {'price_id': p.price_id,
                         'class_length': p.class_length,
                         'price': p.price}

            userdata['existing_prices'].append(new_price)

        return jsonify(userdata)

    return ''


@app.route('/config', methods=['POST'])
def config():
    if request.method == 'POST':

        payload = request.data.decode('utf8')
        data = json.loads(payload)

        with open('testfile.txt', 'w') as f:
            json.dump(data, f)

        try:
            jwt.decode(data['token'], app.config['SECRET_KEY'], algorithms='HS256')

        except jwt.ExpiredSignatureError:
            return "Token has expired, please log in again"

        except (jwt.DecodeError, jwt.InvalidTokenError):
            return "Invalid token provided"

        userdata={}

        if data['type'] == 'reschedule':
            config = Config.query.first()

            if 'numberAllowed' not in data:
                data['numberAllowed'] = None

            if 'notice' not in data:
                data['notice'] = None

            if Config.query.first() is None:

                config = Config(reschedules_allowed=data['numberAllowed'] if data['numberAllowed'] is not '' else None,
                                notice_required=data['notice'] if data['notice'] is not '' else None)

            else:
                config.reschedules_allowed=data['numberAllowed'] if data['numberAllowed'] is not '' else None
                config.notice_required=data['notice'] if data['notice'] is not '' else None

            db.session.add(config)
            db.session.commit()


        if data['type'] == 'session':

            Session.query.update({Session.current_session: False})
            Session.query.update({Session.next_session: False})

            current_session = Session(start_date=data['currentStartDate'],
                                      end_date=data['currentEndDate'],
                                      current_session=True,
                                      next_session=False)

            next_session = Session(start_date=data['nextStartDate'],
                                   end_date=data['nextEndDate'],
                                   current_session=False,
                                   next_session=True)

            db.session.add(current_session)
            db.session.add(next_session)
            db.session.commit()

        if data['type'] == 'classTypes':

            new_class_type = ClassTypes(class_type = data['classType'],
                                        num_students = data['numStudents'])

            db.session.add(new_class_type)
            db.session.commit()

            class_types = ClassTypes.query.all()
            userdata['existing_classes'] = []

            for ct in class_types:
                new_type = {'class_type_id': ct.class_type_id,
                            'class_type': ct.class_type,
                            'num_students': ct.num_students}

                userdata['existing_classes'].append(new_type)

        if data['type'] == 'price':

            new_price = Prices(class_length = data['classLength'],
                               price = data['price'])

            db.session.add(new_price)
            db.session.commit()

            prices = Prices.query.all()
            userdata['existing_prices'] = []

            for p in prices:
                new_price = {'price_id': p.price_id,
                             'class_length': p.class_length,
                             'price': p.price}

                userdata['existing_prices'].append(new_price)

        userdata['configUpdate'] = True

        return jsonify(userdata)

    return ''


@app.route('/all_classes', methods=['POST'])
def get_all_classes():
    if request.method == 'POST':

        payload = request.data.decode('utf8')
        data = json.loads(payload)

        try:
            jwt.decode(data['token'], app.config['SECRET_KEY'], algorithms='HS256')

        except jwt.ExpiredSignatureError:
            return "Token has expired, please log in again"

        except (jwt.DecodeError, jwt.InvalidTokenError):
            return "Invalid token provided"

        else:

            classes = db.session.query(Classes).join(Students).join(Session).all()
            students = Students.query.all()
            sessions = Session.query.all()

            userdata = {}
            userdata['classes'] = []
            userdata['students'] = []
            userdata['sessions'] = []

            for st in students:
                new_student = {'student_id': st.student_id,
                               'fname': st.fname,
                               'lname': st.lname}

                userdata['students'].append(new_student)

            for c in classes:
                new_class = {'student_id': c.students.student_id,
                             'fname': c.students.fname,
                             'lname': c.students.lname,
                             'class_start': c.class_start.isoformat(),
                             'class_end': c.class_end.isoformat(),
                             'session_id': c.session.session_id,
                             's_start_date': c.session.start_date.isoformat(),
                             's_end_date': c.session.end_date.isoformat(),
                             'current_session': c.session.current_session,
                             'next_session': c.session.next_session
                            }

                userdata['classes'].append(new_class)

            for s in sessions:
                new_session = {'session_id': s.session_id,
                               's_start_date': s.start_date.isoformat(),
                               's_end_date': s.end_date.isoformat(),
                               'current_session': s.current_session,
                               'next_session': s.next_session
                              }

                userdata['sessions'].append(new_session)

            return jsonify(userdata)


@app.route('/add_scheduled_classes', methods=['POST'])
def add_scheduled_classes():
    if request.method == 'POST':

        payload = request.data.decode('utf8')
        data = json.loads(payload)

        with open('testfile.txt', 'w') as f:
            json.dump(data, f)

        try:
            jwt.decode(data['token'], app.config['SECRET_KEY'], algorithms='HS256')

        except jwt.ExpiredSignatureError:
            return "Token has expired, please log in again"

        except (jwt.DecodeError, jwt.InvalidTokenError):
            return "Invalid token provided"

        userdata={}
        session = None

        if data['selectedSession'] == 'current':
            session = Session.query.filter(Session.current_session == True).first()

        elif data['selectedSession'] == 'next':
            session = Session.query.filter(Session.next_session == True).first()
        else:
            data['error'] = 'Selected session not found'

        for c in data['scheduleDates']:

            new_class = Classes(class_start=c[0],
                                class_end=c[1],
                                student_id=data['studentId'],
                                session_id=session.session_id,
                                )

            db.session.add(new_class)

        new_payment = Payments(student_id=data['studentId'],
                               session_id=session.session_id,
                               price=data['price'],
                               paid=False
                               )

        db.session.add(new_payment)

        db.session.commit()

        userdata['classScheduled'] = True

        return jsonify(userdata)

    return ''


@app.route('/get_payment', methods=['POST'])
def get_payment_info():
    if request.method == 'POST':
        payload = request.data.decode('utf8')
        data = json.loads(payload)

        userdata = {}

        with open ('testfile.txt','w') as f:
            json.dump(data, f)

        try:
            token = jwt.decode(data['token'], app.config['SECRET_KEY'], algorithms='HS256')

        except jwt.ExpiredSignatureError:
            return "Token has expired, please log in again"

        except (jwt.DecodeError, jwt.InvalidTokenError):
            return "Invalid token provided"

        else:
            id = data['id']
            s = Students.query.filter(Students.student_id == id).first()
            current_session = Session.query.filter(Session.current_session == True).first()
            next_session = Session.query.filter(Session.next_session == True).first()
            current_status = None
            next_status = None
            current_total = None
            next_total = None
            userdata['current_classes'] = []
            userdata['next_classes'] = []

            for p in s.payments:

                if p.session_id == current_session.session_id:

                    current_status = p.paid
                    current_classes = Classes.query.filter(Classes.student_id == id).filter(
                        Classes.session_id == p.session_id).all()
                    current_total = len(current_classes) * p.price

                    for c in current_classes:

                        new_class = {'class_start': c.class_start,
                                     'class_end': c.class_end
                                     }

                        userdata['current_classes'].append(new_class)

                if p.session_id == next_session.session_id:

                    next_status = p.paid
                    next_classes = Classes.query.filter(Classes.student_id == id).filter(
                        Classes.session_id == p.session_id).all()
                    next_total = len(next_classes) * p.price

                    for c in next_classes:

                        new_class = {'class_start': c.class_start,
                                     'class_end': c.class_end
                                     }

                        userdata['next_classes'].append(new_class)

            userdata['fname'] = s.fname
            userdata['lname'] = s.lname
            userdata['current_start_date'] = current_session.start_date.isoformat()
            userdata['current_end_date'] = current_session.end_date.isoformat()
            userdata['next_start_date'] = next_session.start_date.isoformat()
            userdata['next_start_date'] = next_session.end_date.isoformat()
            userdata['current_status'] = current_status
            userdata['next_status'] = next_status
            userdata['current_total'] = current_total
            userdata['next_total'] = next_total

            return jsonify(userdata)

    return ''


@app.route('/get_reschedule', methods=['POST'])
def get_reschedule():
    if request.method == 'POST':

        payload = request.data.decode('utf8')
        data = json.loads(payload)

        with open('testfile.txt', 'w') as f:
            json.dump(data, f)

        try:
            token = jwt.decode(data['token'], app.config['SECRET_KEY'], algorithms='HS256')

        except jwt.ExpiredSignatureError:
            return "Token has expired, please log in again"

        except (jwt.DecodeError, jwt.InvalidTokenError):
            return "Invalid token provided"

        userdata={}

        user_id = token['user_id']
        user = Users.query.filter(Users.public_id == user_id).first()
        session = Session.query.filter(Session.current_session == True).first()
        today=arrow.now()
        userdata['students'] = []

        for s in user.students:

            current_classes = []

            for c in s.classes:

                if c.class_start.date() >= session.start_date.date() and c.class_start.date() <= session.end_date.date() and c.class_start.date() > today.date():

                    current_classes.append(c.class_start.date().isoformat())

            new_student= {'student_id': s.student_id,
                          'student_name': s.fname + ' ' + s.lname,
                          'classes': current_classes
                          }

            userdata['students'].append(new_student)

        return jsonify(userdata)

    return ''


@app.route('/create_schedule', methods=['POST'])
def create_schedule():
    if request.method == 'POST':

        payload = request.data.decode('utf8')
        data = json.loads(payload)

        with open('testfile.txt', 'w') as f:
            json.dump(data, f)

        try:
            jwt.decode(data['token'], app.config['SECRET_KEY'], algorithms='HS256')

        except jwt.ExpiredSignatureError:
            return "Token has expired, please log in again"

        except (jwt.DecodeError, jwt.InvalidTokenError):
            return "Invalid token provided"

        new_schedule = Schedules(schedule_name=data['scheduleName'],
                                 location_id=data['scheduleLocation'])

        db.session.add(new_schedule)
        db.session.commit()


        userdata={}

        locations = Locations.query.all()
        userdata['locations'] = []

        for l in locations:

            location_list = {'key': l.location_id, 'text': l.location_name, 'value': l.location_id, 'lanes': l.lanes}
            location_list['schedules'] = []

            for ls in l.loc_schedule:
                schedule_list = {'schedule_name': ls.schedule_name, 'schedule_id': ls.schedule_id}
                location_list['schedules'].append(schedule_list)

            userdata['locations'].append(location_list)

        userdata['scheduleUpdate'] = True

        return jsonify(userdata)

    return ''


@app.route('/create_location', methods=['POST'])
def create_location():
    if request.method == 'POST':

        payload = request.data.decode('utf8')
        data = json.loads(payload)

        with open('testfile.txt', 'w') as f:
            json.dump(data, f)

        try:
            jwt.decode(data['token'], app.config['SECRET_KEY'], algorithms='HS256')

        except jwt.ExpiredSignatureError:
            return "Token has expired, please log in again"

        except (jwt.DecodeError, jwt.InvalidTokenError):
            return "Invalid token provided"

        userdata={}

        new_location = Locations(location_name = data['locationName'],
                                 lanes = data['locationLanes']
                                 )

        db.session.add(new_location)
        db.session.commit()

        locations = Locations.query.all()
        userdata['locations'] = []

        for l in locations:

            location_list = {'key': l.location_id, 'text': l.location_name, 'value': l.location_id, 'lanes': l.lanes}
            location_list['schedules'] = []

            for ls in l.loc_schedule:
                schedule_list = {'schedule_name': ls.schedule_name, 'schedule_id': ls.schedule_id}
                location_list['schedules'].append(schedule_list)

            userdata['locations'].append(location_list)

        userdata['locationUpdate'] = True

        return jsonify(userdata)

    return ''


@app.route('/get_schedule_def', methods=['POST'])
def get_schedule_def():
    if request.method == 'POST':

        payload = request.data.decode('utf8')
        data = json.loads(payload)

        with open('testfile.txt', 'w') as f:
            json.dump(data, f)

        try:
            jwt.decode(data['token'], app.config['SECRET_KEY'], algorithms='HS256')

        except jwt.ExpiredSignatureError:
            return "Token has expired, please log in again"

        except (jwt.DecodeError, jwt.InvalidTokenError):
            return "Invalid token provided"

        locations = Locations.query.all()
        class_types = ClassTypes.query.all()
        prices = Prices.query.all()

        userdata={}
        userdata['class_types'] = []
        userdata['class_lengths'] = []
        userdata['locations'] = []
        userdata['prices'] = []

        for l in locations:
            location_list = {'key': l.location_id, 'text': l.location_name, 'value': l.location_id, 'lanes': l.lanes}
            location_list['schedules'] = []

            for ls in l.loc_schedule:
                schedule_list = {'schedule_name': ls.schedule_name, 'schedule_id': ls.schedule_id}
                location_list['schedules'].append(schedule_list)

            userdata['locations'].append(location_list)

        for c in class_types:
            type_list = {'key': c.class_type_id, 'text': c.class_type, 'value': c.class_type_id}
            userdata['class_types'].append(type_list)

        for p in prices:
            class_lengths = {'key': p.price_id, 'text': p.class_length, 'value': p.price_id}
            userdata['class_lengths'].append(class_lengths)


        '''for s in sessions:
            if s.current_session is True:
                session_list = {'key': s.session_id,
                                'text': 'Current Session (' + arrow.get(s.start_date).format('MMM Do') + ' - ' + arrow.get(s.end_date).format('MMM Do') + ')',
                                'value': s.session_id}

                userdata['sessions'].append(session_list)

            if s.next_session is True:
                session_list = {'key': s.session_id,
                                'text': 'Next Session (' + arrow.get(s.start_date).format('MMM Do') + ' - ' + arrow.get(s.end_date).format('MMM Do') + ')',
                                'value': s.session_id}

                userdata['sessions'].append(session_list)
        '''

        return jsonify(userdata)

    return ''


@app.route('/add_schedule_def', methods=['POST'])
def add_schedule_def():
    if request.method == 'POST':

        payload = request.data.decode('utf8')
        data = json.loads(payload)

        with open('testfile.txt', 'w') as f:
            json.dump(data, f)

        try:
            jwt.decode(data['token'], app.config['SECRET_KEY'], algorithms='HS256')

        except jwt.ExpiredSignatureError:
            return "Token has expired, please log in again"

        except (jwt.DecodeError, jwt.InvalidTokenError):
            return "Invalid token provided"

        class_type = ClassTypes.query.filter(ClassTypes.class_type_id == data['classType']).first()
        class_length = Prices.query.filter(Prices.price_id == data['classLength']).first()

        userdata = {}

        new_defn = ScheduleDefinitions(lane = data['lane'],
                                       max_students = class_type.num_students,
                                       min_level = data['minLevel'],
                                       max_level = data['maxLevel'],
                                       class_type_id = data['classType'],
                                       class_length_id = data['classLength'],
                                       class_start = arrow.get(data['startTime']).time(),
                                       class_end = arrow.get(data['startTime']).shift(minutes=+ class_length.class_length).time(),
                                       split_lane = data['split'],
                                       spots_left = class_type.num_students,
                                       schedule_id = data['schedule'])

        db.session.add(new_defn)
        db.session.commit()

        userdata['scheduleUpdate'] = True

        return jsonify(userdata)


    return ''


@app.route('/query_schedule', methods=['POST'])
def query_schedule():
    if request.method == 'POST':

        payload = request.data.decode('utf8')
        data = json.loads(payload)

        with open('testfile.txt', 'w') as f:
            json.dump(data, f)

        try:
            jwt.decode(data['token'], app.config['SECRET_KEY'], algorithms='HS256')

        except jwt.ExpiredSignatureError:
            return "Token has expired, please log in again"

        except (jwt.DecodeError, jwt.InvalidTokenError):
            return "Invalid token provided"

        schedule = Schedules.query.filter(Schedules.schedule_id == data['schedule']).first()

        userdata={}
        userdata['definitions'] = []

        for d in schedule.definitions:
            new_defn = {'lane': d.lane,
                        'max_students': d.max_students,
                        'min_level': d.min_level,
                        'max_level': d.max_level,
                        'class_length': d.class_length.class_length,
                        'class_type': d.class_type.class_type,
                        'class_start': d.class_start.isoformat(),
                        'class_end': d.class_end.isoformat(),
                        'split_lane': d.split_lane,
                        'spots_left': d.spots_left}

            userdata['definitions'].append(new_defn)


        return jsonify(userdata)

    return ''


@app.route('/do_the_schedule', methods= ['GET'])
def do_the_schedule():
    if request.method == 'GET':

        header = request.headers.get('Authorization').split(' ')
        with open('testfile.txt','w') as f:
            for x in header:

                f.write(x + '\n')
                f.write(str(len(header)))

        if len(header) == 2:

            if header[0] == 'Bearer':

                try:
                    token = jwt.decode(header[1], 'secret', algorithms='HS256')
                except jwt.ExpiredSignatureError:
                    return "Token has expired, please log in again"
                except (jwt.DecodeError, jwt.InvalidTokenError):
                    return "Invalid token provided"
                else:
                    with open('testfile.txt','w') as f:
                        f.write(token['user_id'])
                    return "Successfully decoded!"
            return 'Incorrect Authorization Type'

            #schedule = scheduler.do_the_schedule(scheduler.get_students())
            #return jsonify(schedule)
        return 'Authentication error'
    return 'Nothing happened'


if __name__ == "__main__":
    app.run(debug=True)
    #db.create_all()
