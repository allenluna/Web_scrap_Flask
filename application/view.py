from flask import Blueprint, render_template, request
from .controller import SeleniumDriver
view = Blueprint("view", __name__)


@view.route("/")
def home():
    
    return render_template("home.html")


@view.route("/filter-data", methods=["GET", "POST"])
def filter_data():
    
    if request.method == "POST":
        filter = request.json["filter"]
        if filter != "":
            # get generated account
            sig_in = request.json["sign_in"]
            password = request.json["password"]
            
            open_linkedin = SeleniumDriver()
            open_linkedin.login(sig_in, password)
            print("works")
        else:
            return {"message": "You need to search"}
    
    return {"message": "Filtered"}