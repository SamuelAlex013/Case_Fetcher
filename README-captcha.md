# CAPTCHA Strategy

The Delhi High Court website uses a simple text-based CAPTCHA. The value is present in the DOM (not an image or audio). The scraper reads the value directly from the element with Selenium and enters it into the form automatically.

This allows for reliable, automated scraping without the need for external CAPTCHA solving services.
