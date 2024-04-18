from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, Blueprint
from flask_bootstrap import Bootstrap

import scripts.db_helpers as db

routes = Blueprint('routes', __name__)

# Routes
@routes.route('/')
def index():
    return render_template('login.html')

@routes.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    for user in db.get_all_users():
        if user['username'] == username and user['password'] == password:
            if user['role'] == 'doctor':
                return redirect(url_for('doctor_dashboard'))
            elif user['role'] == 'patient':
                return redirect(url_for('patient_dashboard'))
    flash('Nom d\'utilisateur ou mot de passe incorrect.')
    return redirect(url_for('index'))

@routes.route('/dashboard/doctor')
def doctor_dashboard():
    return render_template('doctor_dashboard.html')

@routes.route('/dashboard/patient')
def patient_dashboard():
    return render_template('patient_dashboard.html')

@routes.route('/register')
def register():
    return render_template('register.html')
