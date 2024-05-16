"""
Ce fichier contient des fonctions pour envoyer des requêtes à la base de données.
"""

import json
import os
from operator import itemgetter
from pathlib import Path
from typing import Optional

from dateutil.relativedelta import relativedelta
from rich import print
from scripts.CouchDBClient import CouchDBClient

_client = None
current_dir = Path(os.path.dirname(__file__))
data_dir = current_dir / "data"


def get_client():
    global _client
    if _client is None:
        _client = CouchDBClient()
    return _client


def make_default_db(fict_data = False):
    client = get_client()
    if not 'patients' in client.listDatabases():
        client.reset()
        create_dbs(client)
        populate_vaccine_references(client)
        if fict_data: create_fictive_data(client)

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
    vaccine_refenrences_file_path = data_dir / "vaccine_references.json"

    with open(vaccine_refenrences_file_path, "r", encoding="utf-8") as file:
        vaccine_data = json.load(file)

    for vaccine in vaccine_data:
        client.addDocument("vaccine-references", vaccine)


def create_fictive_data(client):
    """Add fictive data about patients, doctor and measures"""
    # Créer les patients fictifs
    with open(data_dir / "patients_fict.json", "r", encoding="utf-8") as file:
        patients_data = json.load(file)

    for patient in patients_data:
        client.addDocument("patients", patient)

    # Health Records
    with open(data_dir / "HR_fict.json", "r", encoding="utf-8") as file:
        health_records = json.load(file)

    for health_record in health_records:
        health_record["type"] = "measure"
        client.addDocument("patients", health_record)

    # Posologie
    with open(data_dir / "posologie_fict.json", "r", encoding="utf-8") as file:
        posologie = json.load(file)

    for medication in posologie:
        medication["type"] = "medication"
        client.addDocument("patients", medication)

    # Doctors
    with open(data_dir / "doctor_fict.json", "r", encoding="utf-8") as file:
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
        "patients",
        "patients",
        "all",
        "function(doc) { if (doc.type === 'patient') { emit(doc._id, doc); }}",
    )

    # Créer un vue pour patient par email
    client.installView(
        "patients",
        "patients",
        "by_email",
        "function(doc) { if (doc.type === 'patient') { emit(doc.email, doc); }}",
    )

    # Créer la vue pour les données de santé des patients
    client.installView(
        "patients",
        "measure",
        "all",
        "function(doc) { if (doc.type === 'measure') { emit(doc._id, doc); }}",
    )

    # Créer la vue pour les médicaments des patients
    client.installView(
        "patients",
        "medication",
        "all",
        "function(doc) { if (doc.type === 'medication') { emit(doc._id, doc); }}",
    )

    # Créer la vue pour les vaccins des patients
    client.installView(
        "patients",
        "vaccine",
        "all",
        "function(doc) { if (doc.type === 'vaccine') { emit(doc._id, doc); }}",
    )

    # Créer la vue pour les vaccins des patients (trié par patient_id)
    client.installView(
        "patients",
        "vaccine",
        "by_patient_id",
        "function(doc) { if (doc.type === 'vaccine') { emit(doc.patient_id, doc); }}",
    )
    
    # Créer la vue pour les rappels des vaccins des patients
    client.installView(
        "patients",
        "vaccine_reminders",
        "by_patient_id",
        "function(doc) { if (doc.type === 'vaccine_reminders') { emit(doc.patient_id, doc); }}",
    )

    # Créer la vue pour les médecins
    client.installView(
        "doctor", "doctor", "all", "function(doc) { emit(doc._id, doc); }"
    )

    client.installView(
        "doctor", "doctor", "by_email", "function(doc) { emit(doc.email, doc); }"
    )

    # Créer la vue pour les références des vaccins
    client.installView(
        "vaccine-references",
        "vaccine-references",
        "all",
        "function(doc) { emit(doc.vaccines_name, doc); }",
    )


def get_all_patients() -> list:
    client = get_client()
    patients_ = client.executeView("patients", "patients", "all")
    # print("All patients", patients_)
    if len(patients_) == 0:
        return []
    return list(map(itemgetter("value"), patients_))


def get_patient_by_id(patient_id) -> dict:
    client = get_client()
    patient = client.getDocument("patients", patient_id)
    return patient


def get_doctor_notifications() -> list:
    client = get_client()
    doctors = client.executeView("doctor", "doctor", "all")
    # print("Notifications", doctors)
    if len(doctors) == 0:
        return []
    return # doctors[0]["value"]["notifications"]


def get_appointments() -> list:
    client = get_client()
    appointments = client.executeView("doctor", "doctor", "all")
    # print("Appointments", appointments)
    if len(appointments) == 0:
        return []
    return appointments[0]["value"]["appointments"]


def get_patient_health_data() -> dict:
    client = get_client()
    health_data_ = client.executeView("patients", "measure", "all")
    # print("Health data", health_data_)

    if health_data_:
        return health_data_[0]["value"]
    else:
        return {}


def add_vaccines_reminders(vaccine) -> str:
    client = get_client()
    vaccine["type"] = "vaccine_reminders"
    vaccine["is-done"] = False
    key = client.addDocument("patients", vaccine)
    return key


def add_vaccines(vaccine) -> str:
    client = get_client()
    vaccine["type"] = "vaccine"
    key = client.addDocument("patients", vaccine)
    return key


def get_patient_vaccines(patient_id=None) -> list:
    client = get_client()
    patient_vaccines_ = client.executeView(
        "patients", "vaccine", "by_patient_id", key=patient_id
    )
    # print("Vaccines", patient_vaccines_)
    if len(patient_vaccines_) == 0:
        return []
    return list(map(itemgetter("value"), patient_vaccines_))

def get_patient_vaccine_reminders(patient_id=None) -> list:
    client = get_client()
    patient_vaccine_reminders_ = client.executeView(
        "patients", "vaccine_reminders", "by_patient_id", key=patient_id
    )
    # print("Vaccine reminders", patient_vaccine_reminders_)
    if len(patient_vaccine_reminders_) == 0:
        return []
    return list(map(itemgetter("value"), patient_vaccine_reminders_))

def get_all_vaccines_ref() -> list:
    client = get_client()
    vaccines = client.executeView("vaccine-references", "vaccine-references", "all")
    # print("Vaccines", vaccines)
    if len(vaccines) == 0:
        return []
    return list(map(itemgetter("value"), vaccines))

def add_vaccine_ref(vaccine) -> str:
    client = get_client()
    key = client.addDocument("vaccine-references", vaccine)
    return key

def get_frequency_of_vaccine(vaccine_name) -> Optional[relativedelta]:
    client = get_client()
    vaccines = client.executeView(
        "vaccine-references", "vaccine-references", "all", key=vaccine_name
    )
    if len(vaccines) == 0:
        return None
    return relativedelta(years=vaccines[0]["value"]["frequency"])
    

# ========================================================


def patient_already_exists(email) -> bool:
    client = get_client()
    patient = client.executeView("patients", "patients", "by_email", key=email)
    return len(patient) > 0


def get_patient_by_email(email) -> dict:
    client = get_client()
    patient = client.executeView("patients", "patients", "by_email", key=email)
    if len(patient) == 0:
        return {}
    return patient[0]["value"]


def doctor_already_exists(email) -> bool:
    client = get_client()
    doctor = client.executeView("doctor", "doctor", "by_email", key=email)
    return len(doctor) > 0


def get_doctor_by_email(email) -> dict:
    client = get_client()
    doctor = client.executeView("doctor", "doctor", "by_email", key=email)
    if len(doctor) == 0:
        return {}
    return doctor[0]["value"]
