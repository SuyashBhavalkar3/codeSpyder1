from flask import Blueprint, render_template, request, redirect, url_for
from .models import Customer
from app.extensions import db

customers_bp = Blueprint("customers", __name__, template_folder="templates")

@customers_bp.route("/")
def manage_customers():
    customers = Customer.query.all()
    return render_template("manage_customer.html", customers = customers)

@customers_bp.route("/add", methods=["GET", "POST"])
def add_customer():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")  # NEW

        new_customer = Customer(name=name, email=email, password=password)
        db.session.add(new_customer)
        db.session.commit()
        return redirect(url_for("customers.manage_customers"))

    return render_template("edit_customer.html", customer=None)


@customers_bp.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_customer(id):
    customer = Customer.query.get_or_404(id)
    if request.method == "POST":
        customer.name = request.form["name"]
        customer.email = request.form["email"]
        db.session.commit()
        return redirect(url_for("customers.manage_customers"))
    return render_template("edit_customer.html", customer=customer)