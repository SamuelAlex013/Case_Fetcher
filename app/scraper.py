from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from app.models import insert_query
import time
from bs4 import BeautifulSoup

def scrape_court_cases(case_type, case_number, filling_year):
    driver = None
    try:
        options = webdriver.ChromeOptions()
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--headless')  # Run in headless mode for Docker
        options.add_argument('--disable-gpu')
        options.add_argument('--window-size=1920,1080')
        
       
        driver = webdriver.Chrome(options=options)

        driver.get("https://dhcmisc.nic.in/pcase/guiCaseWise.php")

        wait = WebDriverWait(driver, 10)

        # Select case type
        case_type_dropdown = wait.until(EC.presence_of_element_located((By.ID, "ctype")))
        select = Select(case_type_dropdown)
        select.select_by_value(case_type)

        # Case number
        case_number_input = wait.until(EC.presence_of_element_located((By.ID, "regno")))
        case_number_input.clear()
        case_number_input.send_keys(case_number)

        # Filing year (dropdown)
        filling_year_dropdown = wait.until(EC.presence_of_element_located((By.ID, "regyr")))
        year_select = Select(filling_year_dropdown)
        year_select.select_by_value(str(filling_year))

        # CAPTCHA handling - extract from label element
        captcha_input = wait.until(EC.presence_of_element_located((By.NAME, "captcha_code")))
        captcha_input.clear()
        
        # Get CAPTCHA value from the cap label element
        captcha_element = wait.until(EC.presence_of_element_located((By.ID, "cap")))
        captcha_value = captcha_element.text
        
            
        captcha_input.send_keys(captcha_value.strip())

        # Submit the form
        submit_button = wait.until(EC.element_to_be_clickable((By.NAME, "Submit")))
        submit_button.click()

        time.sleep(5)  # Wait for the results to load
        raw_response = driver.page_source

        # Try to get PDF links by clicking Listing Details button only
        pdf_links = []
        try:
            # Look for Listing Details button and click it
            listing_button = driver.find_element(By.NAME, "listing")
            if listing_button:
                listing_button.click()
                time.sleep(5)  # Increased wait time for server response
                
                # Check if we got an error page instead of listing details
                page_source = driver.page_source
                if "PostgreSQL" in page_source or "Fatal error" in page_source or "Warning:" in page_source:
                    print("Court website database error - PDF links not available")
                    pdf_links = []  # No PDF links available due to server error
                else:
                    soup = BeautifulSoup(page_source, "html.parser")
                    
                    # Look for specific PDF download links
                    for a in soup.find_all("a", href=True):
                        href = a["href"]
                        # Check for various PDF link patterns
                        if  "downloadorder" in href.lower():
                            pdf_links.append(href)
                            

        except Exception as e:
            print(f"Error clicking listing details: {e}")
            pass  # If listing details button doesn't work, continue

        if driver:
            driver.quit()
        
        return {
            "raw_response": raw_response,
            "pdf_links": pdf_links
        }

    except Exception as e:
        if driver:
            driver.quit()
        return {"error": str(e)}
    

def parse_court_cases(response_data, case_type=None, case_number=None, filling_year=None):
    # Handle both old format (string) and new format (dict)
    if isinstance(response_data, str):
        raw_response = response_data
        extracted_pdf_links = []
    else:
        raw_response = response_data.get("raw_response", "")
        extracted_pdf_links = response_data.get("pdf_links", [])
    
    soup = BeautifulSoup(raw_response, "html.parser")
    result = {
        "parties": None,
        "filing_date": None,
        "next_hearing_date": None,
        "pdf_links": [],
        "case_status": None,
        "case_number": None
    }

    # Use input parameters to construct case number
    if case_type and case_number and filling_year:
        result["case_number"] = f"{case_type}-{case_number}/{filling_year}"

    # Extract parties - look for the specific table structure with "Vs."
    party_tables = soup.find_all("table", {"bgcolor": "#fff"})
    for table in party_tables:
        rows = table.find_all("tr")
        petitioner = None
        respondent = None
        
        for i, row in enumerate(rows):
            cell = row.find("td", {"align": "center"})
            if cell:
                text = cell.get_text(strip=True)
                # Look for the row with "Vs." - petitioner is in this row
                if "Vs." in text:
                    # Extract petitioner (before "Vs.")
                    petitioner = text.replace("Vs.", "").strip()
                    # Look for respondent in the next row
                    if i + 1 < len(rows):
                        next_cell = rows[i + 1].find("td", {"align": "center"})
                        if next_cell:
                            respondent = next_cell.get_text(strip=True)
                    break
        
        if petitioner and respondent:
            result["parties"] = f"{petitioner} vs {respondent}"
            break

    # Extract dates from table rows - look for specific labels
    all_fonts = soup.find_all("font")
    for i, font in enumerate(all_fonts):
        text = font.get_text(strip=True)
        
        # Filing date
        if "Date of Filing" in text and not result["filing_date"]:
            # Look for the next font element that contains the date
            for j in range(i+1, min(i+5, len(all_fonts))):
                next_text = all_fonts[j].get_text(strip=True)
                if next_text and len(next_text) > 5:  # Basic date validation
                    result["filing_date"] = next_text
                    break
        
        # Next hearing date / Disposal date
        if ("Date of Disposal" in text or "Next Date" in text) and not result["next_hearing_date"]:
            # Look for the next font element that contains the date
            for j in range(i+1, min(i+5, len(all_fonts))):
                next_text = all_fonts[j].get_text(strip=True)
                if next_text and len(next_text) > 5:  # Basic date validation
                    result["next_hearing_date"] = next_text
                    break
        
        # Case status
        if "Status" in text and not result["case_status"]:
            # Look for the next font element that contains the status
            for j in range(i+1, min(i+5, len(all_fonts))):
                next_text = all_fonts[j].get_text(strip=True)
                if next_text and len(next_text) > 1:
                    result["case_status"] = next_text
                    break

    # Use the PDF links extracted by the scraper
    result["pdf_links"] = extracted_pdf_links
    result["pdf_link"] = extracted_pdf_links[-1] if extracted_pdf_links else None

    return result