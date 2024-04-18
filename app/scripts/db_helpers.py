

# Données fictives pour démonstration
# Il faut mettre un CouchDB ici normalement


# Utilisateurs fictifs pour démonstration
users = [
    {'username': 'admin', 'password': 'admin', 'role': 'doctor'},
    {'username': 'user1', 'password': 'password', 'role': 'patient'}
]


# Données fictives des patients
patients_data = [
    {"name": "Jean Dupont", "age": 45, "last_visit": "2022-04-01"},
    {"name": "Marie Martin", "age": 32, "last_visit": "2022-03-28"},
    {"name": "Pierre Dubois", "age": 50, "last_visit": "2022-03-15"}
]

# Rappels et notifications fictifs pour le médecin
doctor_notifications = [
    {"message": "Rappel: Rendez-vous avec Jean Dupont le 2022-04-15"},
    {"message": "Rappel: Vaccination de Marie Martin le 2022-04-20"}
]

# Rendez-vous fictifs avec les patients
appointments_data = [
    {"patient": "Jean Dupont", "date": "2022-04-15", "time": "10h00"},
    {"patient": "Marie Martin", "date": "2022-04-20", "time": "14h30"}
]


# Données fictives pour démonstration
patient_health_data = {
    "temperature": 37.5,
    "heartRate": 72,
    "bloodPressure": "120/80",
    "weight": 75,
    "height": 175
}

patient_reminders = [
    {"type": "Medication", "message": "Prendre le médicament XYZ à 8h00 tous les jours."},
    {"type": "Appointment", "message": "Rendez-vous avec le médecin le 15/04/2024 à 14h00."}
]

patient_medications = [
    {"name": "Médicament XYZ", "dosage": "2 comprimés", "schedule": "Matin"},
    {"name": "Vaccin ABC", "dosage": "1 dose", "schedule": "20/04/2024"}
]

# Mega sécurisé tqt
def get_all_users():
    return users

def get_all_patients():
    return patients_data

def get_doctor_notifications():
    return doctor_notifications

def get_appointments():
    return appointments_data

def get_patient_health_data():
    return patient_health_data

def get_patient_reminders():
    return patient_reminders

def get_patient_medications():
    return patient_medications