from flask import render_template, request, redirect, url_for, flash, Blueprint, session

import scripts.db_helpers as db

routes = Blueprint("routes", __name__)


def check_auth():
    if "loggedin" not in session or not session["loggedin"]:
        return False
    return True


def is_doctor():
    if "role" in session and session["role"] == "doctor":
        return True
    return False


def is_patient():
    if "role" in session and session["role"] == "patient":
        return True
    return False


# Routes
@routes.route("/")
def index():
    if check_auth():
        if session["role"] == "patient":
            return redirect(url_for("routes.patient_dashboard"))
        elif session["role"] == "doctor":
            return redirect(url_for("routes.doctor_vaccination"))
    return render_template("login.html")


@routes.route("/register")
def register():
    return render_template("register.html")


@routes.route("/dashboard/doctor")
def doctor_dashboard():
    if not is_doctor():
        return redirect(url_for("routes.index"))
    return render_template("doctor_dashboard.html")


@routes.route("/doctor/vaccination")
def doctor_vaccination():
    if not is_doctor():
        return redirect(url_for("routes.index"))
    return render_template("doctor_vaccination.html")

@routes.route("/doctor/vaccination_ref")
def doctor_vaccination_ref():
    if not is_doctor():
        return redirect(url_for("routes.index"))
    return render_template("vaccine_references.html")

@routes.route("/dashboard/patient")
def patient_dashboard():
    if not is_patient():
        return redirect(url_for("routes.index"))
    return render_template("patient_dashboard.html")


@routes.route("/patient/vaccination")
def patient_vaccination():
    if not is_patient():
        return redirect(url_for("routes.index"))
    return render_template("patient_vaccination.html")
