"""
Ce fichier contient des fonctions pour envoyer des requêtes à la base de données.
"""

from operator import itemgetter

from rich import print
from scripts.CouchDBClient import CouchDBClient
import json
import os

_client = None
current_dir = os.path.dirname(__file__)

def get_client():
    global _client
    if _client is None:
        _client = CouchDBClient()
    return _client


def make_default_db():
    client = get_client()
    client.reset()
    # if not 'users' in client.listDatabases():
    create_dbs(client)
    populate_vaccine_references(client)
    create_fictive_data(client)

    make_all_view(client)


def create_dbs(client):
    """
    Creates the 3 databases used in this app:
        * patients
        * doctor
        * vaccine-references
    """
    client = get_client()
    client.createDatabase("patients")
    client.createDatabase("doctor")
    client.createDatabase("vaccine-references")

def populate_vaccine_references(client):
    """Add vaccine-references data into the corresponding database"""
    vaccine_refenrences_file_path = os.path.join(current_dir, 'data', 'vaccine_references.json')

    with open(vaccine_refenrences_file_path, 'r') as file:
        vaccine_data = json.load(file)

    for vaccine in vaccine_data:
        client.addDocument("vaccine-references", vaccine)

def create_fictive_data(client):
    """Add fictive data about patients, doctor and measures"""
    # Créer les patients fictifs
    with open(os.path.join(current_dir, 'data', 'patients_fict.json'), 'r') as file:
        patients_data = json.load(file)

    for patient in patients_data:
        client.addDocument("patients", patient)
        
    # Health Records
    with open(os.path.join(current_dir, 'data', 'HR_fict.json'), 'r') as file:
        health_records = json.load(file)
        
    for health_record in health_records:
        health_record["type"] = "measure"
        client.addDocument("patients", health_record)
        
    # Posologie
    with open(os.path.join(current_dir, 'data', 'posologie_fict.json'), 'r') as file:
        posologie = json.load(file)
        
    for medication in posologie:
        medication["type"] = "medication"
        client.addDocument("patients", medication)
    
    # Doctors
    with open(os.path.join(current_dir, 'data', 'doctor_fict.json'), 'r') as file:
        doctor_inami = json.load(file)
        
    # Créer les notifications fictives pour le médecin
    for doctor in doctor_inami:
        client.addDocument("doctor", doctor)

def make_all_view(client):
    """Add all views to the db that retrieve all ...
        * patient json
        * emails of each patients
        * measure json 
        * medication json
        * vaccine json
        * ...
    """
    # Créer la vue pour les patients
    client.installView(
        "patients", "patients", "all",
        "function(doc) { if (doc.type === 'patient') { emit(doc._id, doc); }}"
    )
    
    # Créer un vue pour patient par email
    client.installView(
        "patients", "patients", "by_email",
        "function(doc) { if (doc.type === 'patient') { emit(doc.email, doc); }}"
    )
    
    # Créer la vue pour les données de santé des patients
    client.installView(
        "patients", "measure", "all",
        "function(doc) { if (doc.type === 'measure') { emit(doc._id, doc); }}"
    )
    
    # Créer la vue pour les médicaments des patients
    client.installView(
        "patients", "medication", "all",
        "function(doc) { if (doc.type === 'medication') { emit(doc._id, doc); }}"
    )
    
    # Créer la vue pour les vaccins des patients
    client.installView(
        "patients", "vaccine", "all",
        "function(doc) { if (doc.type === 'vaccine') { emit(doc._id, doc); }}"
    )
    
    # Créer la vue pour les vaccins des patients (trié par patient_id)
    client.installView(
        "patients", "vaccine", "by_patient_id",
        "function(doc) { if (doc.type === 'vaccine') { emit(doc.patient_id, doc); }}"
    )

    # Créer la vue pour les médecins
    client.installView(
        "doctor",
        "doctor",
        "all",
        "function(doc) { emit(doc._id, doc); }"
    )
    
    client.installView(
        "doctor",
        "doctor",
        "by_email",
        "function(doc) { emit(doc.email, doc); }"
    )
    
    # Créer la vue pour les références des vaccins
    client.installView(
        "vaccine-references",
        "vaccine-references",
        "all",
        "function(doc) { emit(doc._id, doc); }"
    )

def get_all_patients():
    client = get_client()
    patients_ = client.executeView("patients", "patients", "all")
    # print("All patients", patients_)
    # TODO manage empty case ?
    return list(map(itemgetter("value"), patients_))

def get_patient_by_id(patient_id):
    client = get_client()
    patient = client.getDocument("patients", patient_id)
    return patient

def get_doctor_notifications():
    client = get_client()
    doctors = client.executeView("doctor", "doctor", "all")
    # print("Notifications", doctors)
    # TODO manage empty case ?
    return doctors[0]["value"]["notifications"]

def get_appointments():
    client = get_client()
    appointments = client.executeView("doctor", "doctor", "all")
    # print("Appointments", appointments)
    # TODO manage empty case ?
    return appointments[0]["value"]["appointments"]

def get_patient_health_data():
    client = get_client()
    health_data_ = client.executeView("patients", "measure", "all")
    # print("Health data", health_data_)

    if health_data_:
        return health_data_[0]["value"]
    else:
        return None 


# def get_patient_reminders():
#     client = get_client()
#     patient_reminders_ = client.executeView("patients", "patients", "all")
#     # print("Reminders", patient_reminders_)
#     return patient_reminders_[0]["value"]["reminders"]


# def get_patient_medications():
#     client = get_client()
#     patient_medications_ = client.
#     # print("Medications", patient_medications_)
#     return patient_medications_[0]["value"]


def add_vaccines(vaccine) -> str:
    client = get_client()
    vaccine["type"] = "vaccine"
    key = client.addDocument("patients", vaccine)
    return key

def get_patient_vaccines(patient_id=None):
    client = get_client()
    patient_vaccines_ = client.executeView("patients", "vaccine", "by_patient_id", key=patient_id)
    # print("Vaccines", patient_vaccines_)
    return list(map(itemgetter("value"), patient_vaccines_))

def get_all_vaccines_ref():
    client = get_client()
    vaccines = client.executeView("vaccine-references", "vaccine-references", "all")
    # print("Vaccines", vaccines)
    return list(map(itemgetter("value"), vaccines))

# ========================================================

def patient_already_exists(email) -> bool:
    client = get_client()
    patient = client.executeView("patients", "patients", "by_email", key=email)
    return len(patient) > 0

def get_patient_by_email(email):
    client = get_client()
    patient = client.executeView("patients", "patients", "by_email", key=email)
    if len(patient) == 0:
        return None
    return patient[0]["value"]

def doctor_already_exists(email) -> bool:
    client = get_client()
    doctor = client.executeView("doctor", "doctor", "by_email", key=email)
    return len(doctor) > 0

def get_doctor_by_email(email):
    client = get_client()
    doctor = client.executeView("doctor", "doctor", "by_email", key=email)
    if len(doctor) == 0:
        return None
    return doctor[0]["value"]