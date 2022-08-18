"""
    Main file for online bank project
    Author: Samuels, Goods,Pearson,and Garber
    Class: CMSC 495-6981
    Date Created: 2022-07-18
    Last Updated: 2022-08-10
"""
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash
from file_methods import create, verify, change, update_balance

#Tracks the logged-in user
LOGGED_IN = None
BALANCE = 0

#Initialize Flask app
app = Flask(__name__)
app.secret_key = "secret"

@app.route("/")
def index():
    """
    Main landing page
    """
    return render_template("index.html", cur_date=datetime.now())

@app.route("/hello/")
def hello(name=None):
    """
    Page prints hello <name>
    """
    return render_template("hello.html", name=name)
    
@app.route("/home/", methods=["GET", "POST"])
def home(current_user=None):
    """
    Home page after logging in
    """
    
    #Update balance
    if request.method == "POST":
        deposit = float(request.form["deposit"] or 0)
        withdraw = float(request.form["withdraw"] or 0)
        global BALANCE
        if BALANCE + deposit - withdraw < 0:
            flash("Withdraw amount cannot exceed balance.")
        else:
            BALANCE += deposit - withdraw
            update_balance(LOGGED_IN, BALANCE)
    
    #User must be logged in to view page
    if LOGGED_IN:
        return render_template("home.html", name=LOGGED_IN, balance="{:.2f}".format(BALANCE))
    return redirect(url_for("login"))

@app.route("/register/", methods=["GET", "POST"])
def register():
    """
    Render method for register page
    """
    if request.method == "POST":
        error = create(request.form["username"], request.form["password"])

        if error is None:
            flash("User successfully registered.")
            return redirect("/login/")
        flash(error)

    return render_template("register.html")

@app.route("/login/", methods=["GET", "POST"])
def login():
    """
    Render method for login page
    """
    if request.method == "POST":
        global BALANCE
        BALANCE = verify(request.form["username"], request.form["password"])
        if BALANCE > -1:
            global LOGGED_IN
            LOGGED_IN = request.form["username"]
            flash("Successfully logged in.")
            return redirect("/home/")

        flash("Invalid username or password.")

    return render_template("login.html")
    
@app.route("/update/", methods=["GET", "POST"])
def update():
    """
    Render method for update page
    """
    if request.method == "POST":
        if request.form["password"] != request.form["confirm"]:
            error = "Passwords do not match."
        else:
            error = change(LOGGED_IN, request.form["password"])

        if error is None:
            flash("Successfully updated password.")
            return redirect("/home/")

        flash(error)

    return render_template("update.html", LOGGED_IN=LOGGED_IN)


@app.route("/logout/", methods=["GET", "POST"])
def logout():
    """
    Render method for logging out
    """
    
    global LOGGED_IN
    LOGGED_IN = None
    flash("Successfully logged out.")
    return redirect("/")