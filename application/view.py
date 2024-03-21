from flask import Blueprint, render_template, request, jsonify
from .controller import SeleniumDriver


view = Blueprint("view", __name__)


@view.route("/")
def home():
    
    return render_template("home.html")


@view.route("/filter-data", methods=["GET", "POST"])
def filter_data():
    # Access data from local storage sent from client-side
    local_data = request.json.get("localData", None)
    if request.method == "POST":
        try:
            # Get the JSON data from the request body
            request_data = request.get_json()
            filter = request_data.get("filter", "")
            if filter != "":
                # get generated account
                sig_in = request_data["sign_in"]
                password = request_data["password"]
                
                open_linkedin = SeleniumDriver()
                try:
                    open_linkedin.login(sig_in, password)
                    parsed_data = open_linkedin.filter_employee()
                    # Store the parsed data in the local storage
                    
                    return jsonify({"message": "Resumes Downloaded", "data": parsed_data})
                    
                except TimeoutError:
                    print("Error network")

            else:
                return {"message": "You need to search"}
        except Exception as e:
            print(f"Error: {e}")

    return {"message": local_data}

