"""
Ce fichier contient des fonctions pour envoyer des requêtes à la base de données.
"""

from operator import itemgetter

from rich import print
from scripts.CouchDBClient import CouchDBClient

_client = None


def get_client():
    global _client
    if _client is None:
        _client = CouchDBClient()
    return _client


def make_default_db():
    client = get_client()
    # if not 'users' in client.listDatabases():
    create_fictive_data()
    make_all_view()


def create_fictive_data():
    client = get_client()

    client.reset()

    p_keys = []
    # Créer les patients fictifs
    client.createDatabase("patients")
    for patient in patients_data:

        key = client.addDocument("patients", patient)
        p_keys.append(key)

    d_keys = []
    # Créer les notifications fictives pour le médecin
    client.createDatabase("doctor")

    for doctor in doctor_inami:
        for i, appointment in enumerate(doctor["appointments"]):
            appointment["patient_id"] = p_keys[i]

        key = client.addDocument("doctor", doctor)
        d_keys.append(key)

    v_keys = []
    client.createDatabase("vaccine-reference")
    for vaccine in vaccine_ref:
        key = client.addDocument("vaccine-reference", vaccine)
        v_keys.append(key)


def make_all_view():
    client = get_client()

    # Créer la vue pour les patients
    client.installView(
        "patients", "patients", "all",
        "function(doc) { if (doc.type === 'patient') { emit(doc._id, doc); }}"
        
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

    # Créer la vue pour les médecins
    client.installView(
        "doctor",
        "doctor",
        "all",
        "function(doc) { emit(doc._id, doc); }"
    )


health_records = [
    {
        "type": "measure",
        "temperature": 37.5,
        "heartRate": 72,
        "bloodPressure": "120/80",
        "weight": 75,
        "height": 175,
    }
]

posologie = [
    {
        "type": "medication",
        "name": "Médicament XYZ",
        "dosage": "2 comprimés",
        "schedule": "Matin",
    },
]

# Données fictives des patients
patients_data = [
    {
        "type": "patient",
        "name": "Jean Dupont",
        "birthdate": "29/2/2000",
        "last_visit": "2022-04-01",
    },
    {
        "type": "patient",
        "name": "Marie Martin",
        "birthdate": "29/2/2000",
        "last_visit": "2022-03-28",
    },
    {
        "type": "patient",
        "name": "Pierre Dubois",
        "birthdate": "29/2/2000",
        "last_visit": "2022-03-15",
    },
]


# Données fictives pour le médecin
doctor_inami = [
    {
        "inami": "123456",
        "name": "Dr. Dupont",
        "notifications": [
            {"message": "Rappel: Rendez-vous avec Jean Dupont le 2022-04-15"},
            {"message": "Rappel: Vaccination de Marie Martin le 2022-04-20"},
        ],
        "appointments": [
            {
                "patient_id": -1,
                "patient": "Jean Dupont",
                "date": "2022-04-15",
                "time": "10h00",
                "reason": "Consultation",
            },
            {
                "patient_id": -2,
                "patient": "Marie Martin",
                "date": "2022-04-20",
                "time": "14h30",
                "reason": "Vaccination",
            },
        ],
    },
    {
        "inami": "654321",
        "name": "Dr. Martin",
        "notifications": [
            {"message": "Rappel: Rendez-vous avec Pierre Dubois le 2022-04-15"},
            {"message": "Rappel: Vaccination de Jean Dupont le 2022-04-20"},
        ],
        "appointments": [
            {
                "patient_id": -3,
                "patient": "Pierre Dubois",
                "date": "2022-04-15",
                "time": "10h00",
                "reason": "Consultation",
            },
            {
                "patient_id": -1,
                "patient": "Jean Dupont",
                "date": "2022-04-20",
                "time": "14h30",
                "reason": "Vaccination",
            },
        ],
    },
]

vaccine_ref = [
    {
        "name":"Tétanos", 
        "frequency": 10, 
        "doses": [2]
    }, 
    {
        "name":"Diphtérie", 
        "frequency": 10, 
        "doses": [2]
    },
    {
        "name":"Coqueluche", 
        "frequency": 10, 
        "doses": [2]
    },
    {
        "name":"RRO (Rougeole, Rubéole, Oreillons)", 
        "frequency": 0, 
        "dose": [12, 12*7]
    }
]

def get_all_patients():
    client = get_client()
    patients_ = client.executeView("patients", "patients", "all")
    # print("All patients", patients_)
    return list(map(itemgetter("value"), patients_))

def get_patient_by_id(patient_id):
    client = get_client()
    patient = client.getDocument("patients", patient_id)
    return patient

def get_doctor_notifications():
    client = get_client()
    doctors = client.executeView("doctor", "doctor", "all")
    # print("Notifications", doctors)
    return doctors[0]["value"]["notifications"]


def get_appointments():
    client = get_client()
    appointments = client.executeView("doctor", "doctor", "all")
    # print("Appointments", appointments)
    return appointments[0]["value"]["appointments"]


def get_patient_health_data():
    client = get_client()
    health_data = client.executeView("patients", "measure", "all")
    # print("Health data", health_data)
    return health_data[0]["value"]


# def get_patient_reminders():
#     client = get_client()
#     patient_reminders_ = client.executeView("patients", "patients", "all")
#     # print("Reminders", patient_reminders_)
#     return patient_reminders_[0]["value"]["reminders"]


def get_patient_medications():
    client = get_client()
    patient_medications_ = client.executeView("patients", "medication", "all")
    # print("Medications", patient_medications_)
    return patient_medications_[0]["value"]


def add_vaccines(vaccine) -> str:
    client = get_client()
    vaccine["type"] = "vaccine"
    key = client.addDocument("patients", vaccine)
    return key

def get_patient_vaccines():
    client = get_client()
    patient_vaccines_ = client.executeView("patients", "vaccine", "all")
    # print("Vaccines", patient_vaccines_)
    return list(map(itemgetter("value"), patient_vaccines_))

