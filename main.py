from flask import Flask, request, jsonify
from flask_cors import CORS
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET'])
def home():
    return "API is working"

@app.route('/lookup', methods=['POST'])
def lookup():
    data = request.get_json()
    phone_number = data.get('number')

    if not phone_number:
        return jsonify({"error": "Phone number is required"}), 400

    try:
        # Set up Chrome options
        options = Options()
        options.add_argument('--headless')  # Run in headless mode
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')

        # Set up WebDriver with the appropriate ChromeDriver version
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)

        # Navigate to the website
        driver.get("https://uspeoplesearch.com")
        time.sleep(2)

        # Locate the search input, enter phone number, and click the search button
        search_input = driver.find_element(By.XPATH, '//input[@type="text"]')
        search_input.send_keys(phone_number)

        search_btn = driver.find_element(By.XPATH, '//button[contains(@class, "search-button")]')
        search_btn.click()

        time.sleep(5)  # Wait for the page to load results

        # Extract information from the page
        name = driver.find_element(By.XPATH, '//div[contains(text(), "PERSON NAME")]/following-sibling::div').text
        state = driver.find_element(By.XPATH, '//div[contains(text(), "State")]/following-sibling::div').text
        age = driver.find_element(By.XPATH, '//div[contains(text(), "AGE")]/following-sibling::div').text

        # Return the extracted data in JSON format
        return jsonify({
            "name": name,
            "state": state,
            "age": age
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        driver.quit()  # Ensure the driver is quit at the end

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
