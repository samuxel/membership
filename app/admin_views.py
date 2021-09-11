from app import app
from flask import render_template, session
from app.views import users


@app.route("/admin-dashboard")
def admin_index():
    return "Admin Dashboard!"


@app.route("/admin-about")
def admin_about():
    return render_template("backend.html",values = users.query.all())