from flask import request, jsonify, Blueprint, session, redirect, url_for
import json
import scripts.db_helpers as db

api_auth = Blueprint('api_auth', __name__)


# Route pour récupérer la liste des patients
@api_auth.route('/auth/register', methods=['POST'])
def register():
    data = json.loads(request.get_data())
    
    print(data)
    
    client = db.get_client()
    
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    birthdate = data.get('birthdate')
    role = data.get('role')
    
    if not name or not email or not password or not birthdate or not role:
        return jsonify({'error': 'Missing parameters'}), 400
    
    if role not in ['doctor', 'patient']:
        return jsonify({'error': 'Invalid role'}), 400
    
    if role == 'patient':
        patient = {
            'type': 'patient',
            'name': name,
            'email': email,
            'password': password,
            'birthdate': birthdate
        }
        
        if db.patient_already_exists(email):
            return jsonify({'error': 'Patient already exists'}), 400
        
        key = client.addDocument('patients', patient)
        
        session["id"] = key
        session["role"] = role
        session["name"] = name
        session["loggedin"] = True
        
        return jsonify({'id': key, 'role': role, 'name': name})
    
    elif role == 'doctor':
        
        doctor = {
            'type': 'doctor',
            'name': name,
            'email': email,
            'password': password
        }
        
        if db.doctor_already_exists(email):
            return jsonify({'error': 'Doctor already exists'}), 400
        
        key = client.addDocument('doctor', doctor)
        
        session["id"] = key
        session["role"] = role
        session["name"] = name
        session["loggedin"] = True
        
        return jsonify({'id': key, 'role': role, 'name': name})

    return jsonify({'error': 'Unknown error'}), 500

@api_auth.route('/auth/login', methods=['POST'])
def login():
    
    data = json.loads(request.get_data())
    
    print(data)
    
    email = data.get('email')
    password = data.get('password')
    role = data.get('role')
    
    if not email or not password or not role or role not in ['doctor', 'patient']:
        return jsonify({'error': 'Missing parameters'}), 400
    
    if role == 'patient':
        patient = db.get_patient_by_email(email)
        
        if not patient or patient['password'] != password:
            return jsonify({'error': 'Invalid credentials'}), 401
        
        session["id"] = patient['_id']
        session["role"] = role
        session["name"] = patient['name']
        session["loggedin"] = True
        
        return jsonify({'id': patient['_id'], 'role': role, 'name': patient['name']})
    
    elif role == 'doctor':
        doctor = db.get_doctor_by_email(email)
        
        if not doctor or doctor['password'] != password:
            return jsonify({'error': 'Invalid credentials'}), 401
        
        session["id"] = doctor['_id']
        session["role"] = role
        session["name"] = doctor['name']
        session["loggedin"] = True
        
        return jsonify({'id': doctor['_id'], 'role': role, 'name': doctor['name']})
    
    return jsonify({'error': 'Invalid credentials'}), 401

@api_auth.route('/auth/logout', methods=['GET','POST'])
def logout():
    
    if 'loggedin' in session:
        session.pop('loggedin')
        session.pop('id')
        session.pop('role')
        session.pop('name')
    
    return redirect(url_for('routes.index'))