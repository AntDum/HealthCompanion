import json

import scripts.db_helpers as db
from dateutil.parser import parse
from flask import Blueprint, jsonify, request, session

api_data = Blueprint("api_data", __name__)


def check_auth():
    if "loggedin" not in session or not session["loggedin"]:
        return False
    return True


@api_data.before_request
def before_request():
    if not check_auth():
        return jsonify({"error": "Not authorized"}), 401


# Route pour récupérer la liste des patients
@api_data.route("/api/patients")
def get_patients():
    patients = db.get_all_patients()

    response = [{"id": patient["_id"], "name": patient["name"]} for patient in patients]

    return jsonify(response)


# Route pour récupérer les rappels et notifications pour le médecin
@api_data.route("/api/doctor/notifications")
def get_doctor_notifications():
    return jsonify(db.get_doctor_notifications())


# Route pour récupérer les rendez-vous avec les patients
@api_data.route("/api/appointments")
def get_appointments():
    return jsonify(db.get_appointments())


# Route pour que le médecin puisse envoyer un message au patient
@api_data.route("/api/doctor/message", methods=["POST"])
def send_message_to_patient():
    data = request.get_json()
    message = data["message"]
    # Simuler une réponse du patient pour la démonstration
    response_message = "Merci pour votre message. Je vais bien, merci."
    return jsonify({"message": response_message})

# Nouvelle route pour récupérer les données de santé du patient
@api_data.route("/api/patients/health-data")
def get_patient_health_data():
    return jsonify(db.get_patient_health_data())


# # Nouvelle route pour récupérer les rappels et notifications du patient
# @api_data.route('/api/patients/reminders')
# def get_patient_reminders():
#     return jsonify(db.get_patient_reminders())

# Nouvelle route pour récupérer les médicaments et vaccinations du patient
# @api_data.route('/api/patients/medications')
# def get_patient_medications():
#     return jsonify(db.get_patient_medications())


@api_data.route("/api/patients/vaccine", methods=["POST"])
def add_vaccine():
    data = json.loads(request.get_data())

    patient = db.get_patient_by_id(data["patient_id"])

    if patient is None:
        return jsonify({"error": "Patient not found"})

    vaccine = {
        "date": data["vaccine_date"],
        "name": data["vaccine_name"],
        "patient_name": patient["name"],
        "patient_id": data["patient_id"],
        "doctor_name": data.get("doctor_name", session["name"]),
    }
    db.add_vaccines(vaccine)

    return jsonify({"message": "Vaccine added successfully"})


@api_data.route("/api/patients/vaccine", methods=["GET"])
def get_vaccines():
    return jsonify(db.get_patient_vaccines(session["id"]))

@api_data.route("/api/patients/vaccine_reminders", methods=["GET"])
def get_vaccine_reminders():
    return jsonify(db.get_patient_vaccine_reminders(session["id"]))


@api_data.route("/api/patients/vaccine_reminders", methods=["POST"])
def add_vaccine_reminder():
    data = json.loads(request.get_data())
    
    vaccine_reminders = {
        # TODO (Béa) : C'est ici que tu dois faire le liens avec le front
        "due_date": data["vaccine_reminder_date"],
        "vaccine_name": data["vaccine_name"],
        "patient_name": data["patient_name"],
        "patient_id": data["patient_id"],
        "doctor": session["name"]
    }
    db.add_vaccines_reminders(vaccine_reminders)

    return jsonify({"message": "Vaccine reminder added successfully"})


@api_data.route("/api/vaccine/ref", methods=["GET"])
def get_vaccine_ref():
    return jsonify(db.get_all_vaccines_ref())

@api_data.route("/api/vaccine/ref", methods=["POST"])
def add_vaccine_ref():
    data = json.loads(request.get_data())
    
    vaccine_name = data["vaccine_name"]
    against = [ags.strip() for ags in data["against"].split(",")]
    mandatory = data["mandatory"]
    free = data["free"]
    
    vaccine_ref = {
        "vaccines_name": vaccine_name,
        "against": against,
        "mandatory": {"Belgique":mandatory},
        "free": free,
    }
    db.add_vaccine_ref(vaccine_ref)

    return jsonify({"message": "Vaccine reference added successfully"})
