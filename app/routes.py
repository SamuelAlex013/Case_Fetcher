from flask import Blueprint, render_template, request
from app.scraper import scrape_court_cases
main = Blueprint("main", __name__)

@main.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        case_type = request.form.get("ctype")
        case_number = request.form.get("case_number")
        filling_year = request.form.get("filling_year")
        print(f"Received case type: {case_type}, case number: {case_number}, filling year: {filling_year}")

        raw_response = scrape_court_cases(case_type, case_number, filling_year)
        print(f"Raw response: {raw_response}")

    return render_template("index.html")
