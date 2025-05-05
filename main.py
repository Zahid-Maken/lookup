from flask import Flask, request, jsonify
from flask_cors import CORS
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

# Step 1: Create Flask app
app = Flask(__name__)
CORS(app)

# Step 2: Root route to verify it's working
@app.route('/', methods=['GET'])
def home():
    return "API is working"

# Step 3: POST /lookup route
@app.route('/lookup', methods=['POST'])
def lookup():
    data = request.get_json()
    phone_number = data.get('number')

    if not phone_number:
        return jsonify({"error": "Phone number is required"}), 400

    # Step 4: Configure headless browser
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # Step 5: Launch browser
    driver = webdriver.Chrome(options=chrome_options)

    try:
        # Step 6: Go to site
        driver.get("https://uspeoplesearch.com")  # Replace with your target URL

        time.sleep(2)  # Give page time to load

        # Step 7: Fill form and submit (update XPaths as needed)
        search_input = driver.find_element(By.XPATH, '//input[@type="text"]')
        search_input.send_keys(phone_number)

        search_btn = driver.find_element(By.XPATH, '//button[contains(@class, "search-button")]')
        search_btn.click()

        time.sleep(5)  # Let result load

        # Step 8: Extract results (change XPaths as per actual HTML)
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

# Step 9: Run app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
