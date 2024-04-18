from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, Blueprint
from flask_bootstrap import Bootstrap

import scripts.db_helpers as db

api_data = Blueprint('api_data', __name__)


# Route pour récupérer la liste des patients
@api_data.route('/api/patients')
def get_patients():
    return jsonify(db.get_all_patients())

# Route pour récupérer les rappels et notifications pour le médecin
@api_data.route('/api/doctor/notifications')
def get_doctor_notifications():
    return jsonify(db.get_doctor_notifications())

# Route pour récupérer les rendez-vous avec les patients
@api_data.route('/api/appointments')
def get_appointments():
    return jsonify(db.get_appointments())

# Route pour que le médecin puisse envoyer un message au patient
@api_data.route('/api/doctor/message', methods=['POST'])
def send_message_to_patient():
    data = request.json
    message = data['message']
    # Simuler une réponse du patient pour la démonstration
    response_message = "Merci pour votre message. Je vais bien, merci."
    return jsonify({"message": response_message})

# Nouvelle route pour récupérer les données de santé du patient
@api_data.route('/api/patients/health-data')
def get_patient_health_data():
    return jsonify(db.get_patient_health_data())

# Nouvelle route pour récupérer les rappels et notifications du patient
@api_data.route('/api/patients/reminders')
def get_patient_reminders():
    return jsonify(db.get_patient_reminders())

# Nouvelle route pour récupérer les médicaments et vaccinations du patient
@api_data.route('/api/patients/medications')
def get_patient_medications():
    return jsonify(db.get_patient_medications())
