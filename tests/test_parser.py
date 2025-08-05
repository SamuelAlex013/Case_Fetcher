import pytest
from app.scraper import parse_court_cases

def test_parse_court_cases_basic():
    html = '''<html><body><table bgcolor="#fff"><tr><td align="center">PETITIONER <br>Vs.</td></tr><tr><td align="center">RESPONDENT</td></tr></table><font>Date of Filing : </font><font>01-jan-2023</font><font>Status : </font><font>DISPOSED</font><font>Date of Disposal : </font><font>17-feb-2023</font></body></html>'''
    result = parse_court_cases(html, 'W.P.(C)', '1', '2023')
    assert result['parties'] == 'PETITIONER vs RESPONDENT'
    assert result['filing_date'] == '01-jan-2023'
    assert result['case_status'] == 'DISPOSED'
    assert result['next_hearing_date'] == '17-feb-2023'
