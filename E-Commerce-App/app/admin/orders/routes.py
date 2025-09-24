from flask import Blueprint, render_template, request, redirect, url_for
from .models import Order
from app.extensions import db
from app.admin.customers.models import Customer
from app.admin.products.models import Product

orders_bp = Blueprint("orders", __name__, template_folder="templates")

@orders_bp.route("/")
def manage_orders():
    orders = Order.query.all()
    return render_template("manage_order.html", orders=orders)

@orders_bp.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_order(id):
    order = Order.query.get_or_404(id)
    customers = Customer.query.all()
    products = Product.query.all()

    if request.method == "POST":
        order.customer_id = int(request.form["customer_id"])
        order.product_id = int(request.form["product_id"])
        order.quantity = int(request.form["quantity"])
        db.session.commit()
        return redirect(url_for("orders.manage_orders"))
    return render_template(
        "edit_order.html",
        order = order,
        customers = customers,
        products = products
    )

@orders_bp.route("/add", methods=["GET", "POST"])
def add_order():
    customers = Customer.query.all()
    products = Product.query.all()

    if request.method == "POST":
        customer_id = int(request.form["customer_id"])
        product_id = int(request.form["product_id"])
        quantity = int(request.form["quantity"])
        new_order = Order(
            customer_id = customer_id,
            product_id = product_id,
            quantity = quantity
        )
        db.session.add(new_order)
        db.session.commit()
        return redirect(url_for("orders.manage_orders"))
    
    return render_template(
        "edit_order.html",
        order=None,
        customers = customers,
        products = products
    )