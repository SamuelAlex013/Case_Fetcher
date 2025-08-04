from flask import Blueprint, render_template, request
from app.scraper import scrape_court_cases, parse_court_cases
from app.models import insert_query
main = Blueprint("main", __name__)

@main.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        case_type = request.form.get("ctype")
        case_number = request.form.get("case_number")
        filling_year = request.form.get("filling_year")
        
        # Scrape the court website
        scrape_result = scrape_court_cases(case_type, case_number, filling_year)
        
        # Check if there was an error
        if isinstance(scrape_result, dict) and "error" in scrape_result:
            return render_template("index.html", error=scrape_result["error"])
        
        # Parse the response to extract case details
        parsed_data = parse_court_cases(scrape_result, case_type, case_number, filling_year)
        
        # Store the query in database (extract raw_response if it's a dict)
        if isinstance(scrape_result, dict):
            raw_response_for_db = scrape_result.get("raw_response", "")
        else:
            raw_response_for_db = scrape_result
        insert_query(case_type, case_number, filling_year, raw_response_for_db)
        
        # Render results page with parsed data
        return render_template("results.html", **parsed_data)

    return render_template("index.html")
