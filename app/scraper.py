from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from bs4 import BeautifulSoup

def scrape_court_cases(case_type, case_number, filling_year):
    driver = None
    try:
        options = webdriver.ChromeOptions()
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        
        # Try ChromeDriverManager first, fallback to direct Chrome driver
        try:
            driver = webdriver.Chrome(
                service=Service(ChromeDriverManager().install()),
                options=options
            )
        except Exception:
            # Fallback to direct Chrome driver (assumes chromedriver in PATH)
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

        if driver:
            driver.quit()
        return raw_response

    except Exception as e:
        if driver:
            driver.quit()
        return {"error": str(e)}
    

def parse_court_cases(raw_response):
    soup = BeautifulSoup(raw_response, "html.parser")
    result = {
        "parties": None,
        "filing_date": None,
        "next_hearing_date": None,
        "pdf_links": []
    }

    # 1. Extract parties' names (look for a row or cell containing 'Petitioner' and 'Respondent')
    for table in soup.find_all("table"):
        text = table.get_text(" ", strip=True)
        if "Petitioner" in text and "Respondent" in text:
            # Try to extract parties from the table
            rows = table.find_all("tr")
            for row in rows:
                cols = row.find_all("td")
                if len(cols) >= 2:
                    label = cols[0].get_text(strip=True).lower()
                    value = cols[1].get_text(strip=True)
                    if "petitioner" in label:
                        result["parties"] = value
                    elif "respondent" in label:
                        if result["parties"]:
                            result["parties"] += " vs " + value
                        else:
                            result["parties"] = value

    # 2. Extract filing and next hearing dates
    for table in soup.find_all("table"):
        rows = table.find_all("tr")
        for row in rows:
            cols = row.find_all("td")
            if len(cols) >= 2:
                label = cols[0].get_text(strip=True).lower()
                value = cols[1].get_text(strip=True)
                if "filing date" in label:
                    result["filing_date"] = value
                elif "next date" in label or "next hearing" in label:
                    result["next_hearing_date"] = value

    # 3. Extract PDF links (order/judgment)
    for a in soup.find_all("a", href=True):
        href = a["href"].lower()
        if href.endswith(".pdf"):
            result["pdf_links"].append(a["href"])

    # Only keep the most recent PDF link if available
    if result["pdf_links"]:
        result["pdf_link"] = result["pdf_links"][-1]
    else:
        result["pdf_link"] = None

    return result
