from flask import Flask, request, jsonify
from selenium import webdriver
from pyvirtualdisplay import Display
import boto3

app = Flask(__name__)

# Initialize AWS DynamoDB client
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('TaskAutomationTable')

# Selenium Function for Task Automation
def automate_task(url):
    # Use Xvfb to run Firefox in headless mode
    display = Display(visible=0, size=(800, 600))
    display.start()

    # Initialize Selenium WebDriver with Firefox
    driver = webdriver.Firefox()

    # Implement your Selenium automation logic here
    try:
        driver.get(url)
        
        # Find form elements and fill them out
        name_field = driver.find_element_by_id('name')  # Assuming the input field has id='name'
        email_field = driver.find_element_by_id('email')  # Assuming the input field has id='email'

        # Fill out the form
        name_field.send_keys('John Doe')
        email_field.send_keys('johndoe@example.com')

        # Submit the form
        name_field.submit()

        print("Form submitted successfully!")

    except Exception as e:
        print(f"Error occurred: {e}")

    finally:
        # Close the browser and stop virtual display
        driver.quit()
        display.stop()

# Flask Route for Task Submission
@app.route('/submit-task', methods=['POST'])
def submit_task():
    data = request.get_json()
    task_name = data.get('taskName')
    task_url = data.get('taskURL')

    # Automate the task using Selenium
    automate_task(task_url)

    # Store task data in DynamoDB
    table.put_item(Item={'TaskName': task_name, 'TaskURL': task_url})

    return jsonify({'message': 'Task submitted successfully!'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)
