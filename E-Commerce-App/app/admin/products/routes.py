from flask import Blueprint, render_template, request, redirect, url_for
from .models import Product
from app.extensions import db

products_bp = Blueprint("products", __name__, template_folder="templates")

# List all products
@products_bp.route("/")
def manage_products():
    products = Product.query.all()
    return render_template("manage_product.html", products=products)

# Add a new product
@products_bp.route("/add", methods=["GET", "POST"])
def add_product():
    if request.method == "POST":
        name = request.form.get("name")
        price = float(request.form.get("price", 0))
        stock = int(request.form.get("stock", 0))

        new_product = Product(name=name, price=price, stock=stock)
        db.session.add(new_product)
        db.session.commit()
        return redirect(url_for("products.manage_products"))

    # Render the same template as edit, with product=None
    return render_template("edit_product.html", product=None)

# Edit an existing product
@products_bp.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_product(id):
    product = Product.query.get_or_404(id)

    if request.method == "POST":
        product.name = request.form.get("name")
        product.price = float(request.form.get("price", product.price))
        product.stock = int(request.form.get("stock", product.stock))
        db.session.commit()
        return redirect(url_for("products.manage_products"))

    return render_template("edit_product.html", product=product)
