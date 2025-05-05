from flask import Flask, request, jsonify
from flask_cors import CORS
import chromedriver_autoinstaller
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

app = Flask(__name__)
CORS(app)

# Automatically install the correct version of ChromeDriver
chromedriver_autoinstaller.install()

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
        # Launch headless Chrome using undetected-chromedriver
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')

        # Use the undetected_chromedriver (automatically uses correct version of chromedriver)
        driver = uc.Chrome(options=options)

        # Navigate to the website
        driver.get("https://uspeoplesearch.com")
        time.sleep(2)

        # Locate the search input, enter phone number, and click search button
        search_input = driver.find_element(By.XPATH, '//input[@type="text"]')
        search_input.send_keys(phone_number)

        search_btn = driver.find_element(By.XPATH, '//button[contains(@class, "search-button")]')
        search_btn.click()

        time.sleep(5)

        # Extract information from the page
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
        driver.quit()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
