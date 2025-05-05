from flask import Flask, request, jsonify
from flask_cors import CORS
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
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

    driver = None  # Initialize driver to None to avoid UnboundLocalError

    try:
        # Launch headless Chrome using selenium
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')

        # Specify path to your ChromeDriver
        service = Service('/path/to/chromedriver')  # Update with actual path
        driver = webdriver.Chrome(service=service, options=options)

        driver.get("https://uspeoplesearch.com")
        time.sleep(2)

        search_input = driver.find_element(By.XPATH, '//input[@type="text"]')
        search_input.send_keys(phone_number)

        search_btn = driver.find_element(By.XPATH, '//button[contains(@class, "search-button")]')
        search_btn.click()

        time.sleep(5)

        name = driver.find_element(By.XPATH, '//div[contains(text(), "PERSON NAME")]/following-sibling::div').text
        state = driver.find_element(By.XPATH, '//div[contains(text(), "State")]/following-sibling::div').text
        age = driver.find_element(By.XPATH, '//div[contains(text(), "AGE")]/following-sibling::div').text

        return jsonify({
            "name": name,
            "state": state,
            "age": age
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        if driver:  # Check if driver was initialized
            driver.quit()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
