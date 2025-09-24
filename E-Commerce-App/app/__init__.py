from flask import Flask, render_template, redirect, url_for, request, flash
from .extensions import db, migrate, login_manager
from .config import Config
from app.admin.customers.models import Customer
from flask_login import UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    # Custom User class for Flask-Login
    class CustomerUser(Customer, UserMixin):
        pass

    # User loader for Flask-Login
    @login_manager.user_loader
    def load_user(user_id):
        customer = Customer.query.get(int(user_id))
        if customer:
            return CustomerUser(**customer.__dict__)
        return None

    # -----------------------
    # ROUTES
    # -----------------------

    # Home route: redirects to login or register
    @app.route("/")
    def home():
        if Customer.query.count() == 0:
            return redirect(url_for("register"))
        if current_user.is_authenticated:
            return redirect(url_for("index"))
        return redirect(url_for("login"))

    # Index page (requires login)
    @app.route("/index")
    @login_required
    def index():
        return render_template("index.html")

    # Login page
    @app.route("/login", methods=["GET", "POST"])
    def login():
        if current_user.is_authenticated:
            return redirect(url_for("index"))

        if request.method == "POST":
            email = request.form.get("email")
            password = request.form.get("password")

            user = Customer.query.filter_by(email=email).first()
            if user and check_password_hash(user.password, password):
                login_user(user)
                flash("Logged in successfully!", "success")
                return redirect(url_for("index"))
            else:
                flash("Invalid email or password", "danger")

        return render_template("login.html")

    # Register page
    @app.route("/register", methods=["GET", "POST"])
    def register():
        if current_user.is_authenticated:
            return redirect(url_for("index"))

        if request.method == "POST":
            name = request.form.get("name")
            email = request.form.get("email")
            password = request.form.get("password")

            # Prevent duplicate emails
            if Customer.query.filter_by(email=email).first():
                flash("Email already registered", "warning")
                return redirect(url_for("register"))

            # Create new customer with hashed password
            new_customer = Customer(
                name=name,
                email=email,
                password=generate_password_hash(password)
            )
            db.session.add(new_customer)
            db.session.commit()

            flash("Registration successful! Please log in.", "success")
            return redirect(url_for("login"))

        return render_template("register.html")

    # Logout
    @app.route("/logout")
    @login_required
    def logout():
        logout_user()
        flash("Logged out successfully.", "info")
        return redirect(url_for("login"))

    # -----------------------
    # BLUEPRINTS
    # -----------------------
    from app.admin.customers.routes import customers_bp
    from app.admin.products.routes import products_bp
    from app.admin.orders.routes import orders_bp

    app.register_blueprint(customers_bp, url_prefix="/admin/customers")
    app.register_blueprint(products_bp, url_prefix="/admin/products")
    app.register_blueprint(orders_bp, url_prefix="/admin/orders")

    # Flask-Login configuration
    login_manager.login_view = "login"
    login_manager.login_message_category = "warning"

    return app
