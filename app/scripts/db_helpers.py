"""
Ce fichier contient des fonctions pour envoyé des requêtes à la base de données.
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

    # Créer les utilisateurs fictifs
    client.createDatabase("users")
    for user in users:
        if user["role"] == "patient":
            user["patient_id"] = p_keys.pop()
        elif user["role"] == "doctor":
            user["doctor_id"] = d_keys.pop()

        client.addDocument("users", user)


def make_all_view():
    client = get_client()

    # Créer la vue pour les utilisateurs
    client.installView("users", "users", "all", "function(doc) { emit(doc._id, doc); }")
    client.installView(
        "users",
        "doctor",
        "all",
        "function(doc) { if (doc.role === 'doctor') { emit(doc.username, doc) } }",
    )
    client.installView(
        "users",
        "patient",
        "all",
        "function(doc) { if (doc.role === 'patient') { emit(doc.username, doc) } }",
    )

    # Créer la vue pour les patients
    client.installView(
        "patients", "patients", "all", "function(doc) { emit(doc._id, doc); }"
    )

    # Créer la vue pour les médecins
    client.installView(
        "doctor", "doctor", "all", "function(doc) { emit(doc._id, doc); }"
    )


# Utilisateurs fictifs pour démonstration
users = [
    {"username": "admin", "password": "admin", "role": "doctor"},
    {"username": "user1", "password": "password", "role": "patient"},
]


# Données fictives des patients
patients_data = [
    {
        "name": "Jean Dupont",
        "birthdate": "29/2/2000",
        "last_visit": "2022-04-01",
        "health_data": [
            {
                "temperature": 37.5,
                "heartRate": 72,
                "bloodPressure": "120/80",
                "weight": 75,
                "height": 175,
            }
        ],
        "reminders": [
            {
                "type": "Medication",
                "message": "Prendre le médicament XYZ à 8h00 tous les jours.",
            },
            {
                "type": "Appointment",
                "message": "Rendez-vous avec le médecin le 15/04/2024 à 14h00.",
            },
        ],
        "medications": [
            {"name": "Médicament XYZ", "dosage": "2 comprimés", "schedule": "Matin"},
            {"name": "Vaccin ABC", "dosage": "1 dose", "schedule": "20/04/2024"},
        ],
    },
    {
        "name": "Marie Martin",
        "birthdate": "29/2/2000",
        "last_visit": "2022-03-28",
        "health_data": [
            {
                "temperature": 37.5,
                "heartRate": 72,
                "bloodPressure": "120/80",
                "weight": 75,
                "height": 175,
            }
        ],
        "reminders": [
            {
                "type": "Medication",
                "message": "Prendre le médicament XYZ à 8h00 tous les jours.",
            },
            {
                "type": "Appointment",
                "message": "Rendez-vous avec le médecin le 15/04/2024 à 14h00.",
            },
        ],
        "medications": [
            {"name": "Médicament XYZ", "dosage": "2 comprimés", "schedule": "Matin"},
            {"name": "Vaccin ABC", "dosage": "1 dose", "schedule": "20/04/2024"},
        ],
    },
    {
        "name": "Pierre Dubois",
        "birthdate": "29/2/2000",
        "last_visit": "2022-03-15",
        "health_data": [
            {
                "temperature": 37.5,
                "heartRate": 72,
                "bloodPressure": "120/80",
                "weight": 75,
                "height": 175,
            }
        ],
        "reminders": [
            {
                "type": "Medication",
                "message": "Prendre le médicament XYZ à 8h00 tous les jours.",
            },
            {
                "type": "Appointment",
                "message": "Rendez-vous avec le médecin le 15/04/2024 à 14h00.",
            },
        ],
        "medications": [
            {"name": "Médicament XYZ", "dosage": "2 comprimés", "schedule": "Matin"},
            {"name": "Vaccin ABC", "dosage": "1 dose", "schedule": "20/04/2024"},
        ],
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


# Mega sécurisé tqt
def get_all_users():
    client = get_client()
    users_ = client.executeView("users", "users", "all")
    # print("All users", users_)
    return list(map(itemgetter("value"), users_))


def get_all_patients():
    client = get_client()
    patients_ = client.executeView("patients", "patients", "all")
    # print("All patients", patients_)
    return list(map(itemgetter("value"), patients_))


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
    health_data = client.executeView("patients", "patients", "all")
    # print("Health data", health_data)
    return health_data[0]["value"]["health_data"]


def get_patient_reminders():
    client = get_client()
    patient_reminders_ = client.executeView("patients", "patients", "all")
    # print("Reminders", patient_reminders_)
    return patient_reminders_[0]["value"]["reminders"]


def get_patient_medications():
    client = get_client()
    patient_medications_ = client.executeView("patients", "patients", "all")
    # print("Medications", patient_medications_)
    return patient_medications_[0]["value"]["medications"]
