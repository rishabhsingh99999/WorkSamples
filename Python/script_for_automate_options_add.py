import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
 
# Load your Excel file
# If using CSV, you can use pd.read_csv('yourfile.csv')
df = pd.read_excel('path')  # Adjust the file name and path as needed
 
# Extract existing and new columns
existing_values = df['existing'].dropna().unique()  # Get unique values from the existing column
new_values = df['new'].dropna().unique()  # Get unique values from the new column
 
# Convert to lists for easier manipulation
existing_list = existing_values.tolist()
new_list = new_values.tolist()
 
# Remove values from existing_list that are present in new_list
filtered_existing_list = [value for value in existing_list if value not in new_list]
 
# Update the new_list to remove any values that were found in the existing_list
filtered_new_list = [value for value in new_list if value not in existing_list]
 
# Set up the WebDriver (make sure to specify the correct path to your WebDriver)
driver = webdriver.Chrome()  # or webdriver.Firefox() for Firefox
 
# Jira credentials
jira_url = 'jirs-url'  # Replace with your Jira URL
username = ''  # Replace with your Jira username
password = ''  # Replace with your Jira password
 
# Log into Jira
driver.get(jira_url)
time.sleep(2)  # Wait for the page to load
 
# Find and fill the login form
driver.find_element(By.ID, 'login-form-username').send_keys(username)
driver.find_element(By.ID, 'login-form-password').send_keys(password)
driver.find_element(By.ID, 'login-form-submit').click()
time.sleep(2)  # Wait for the next page to load
 
driver.find_element(By.ID, 'login-form-authenticatePassword').send_keys(password)
driver.find_element(By.ID, 'login-form-submit').click()
time.sleep(10)  # Wait for the dashboard to load
 
results = []
 
for option in filtered_existing_list:
    # Find the <tr> element that contains the <td> with the matching name
    try:
        try:
            message_element = driver.find_element(By.CLASS_NAME, 'aui-message.closeable.aui-message-info')
            # If the message element exists, find the closest button element within it
            close_button = message_element.find_element(By.XPATH, ".//button[contains(@class, 'close')]")  # Adjust the class name as needed
            close_button.click()  # Click the close button
            time.sleep(2)  # Wait for a moment after clicking
        except Exception as e:
            print("No message element found or error occurred:", e)
        # Locate the <tr> containing the <td> with the name
        row = driver.find_element(By.XPATH, f"//tr[td/b[text()='{option}']]")
        # Find the closest <td> that contains the disable button
        disable_button_td = row.find_element(By.XPATH, ".//td//a[contains(@id, 'disable_')]")  # Adjust the class name as needed
        # Click the disable button
        disable_button_td.click()
        time.sleep(2)  # Wait a moment before processing the next option
 
        results.append({'value name': option, 'status': 'disabled'})
    except Exception as e:
        print(f"Error processing option '{option}': {e}")
 
# Add options from the DataFrame
for option in filtered_new_list:
    # Find the input field for adding options
    input_field = driver.find_element(By.NAME, 'addValue')  # Adjust the XPath as needed
    input_field.send_keys(option)
    driver.find_element(By.ID, 'add_submit').click()
    time.sleep(2)  # Wait a moment before adding the next option
    results.append({'value name': option, 'status': 'added'})
 
 
# Save changes
driver.find_element(By.XPATH, "//input[@class='aui-button' and @type='button' and @value='Done']").click()  # Adjust the XPath as needed
time.sleep(5)  # Wait for the save action to complete
 
# Close the browser
driver.quit()
 
# Create a DataFrame from the results
results_df = pd.DataFrame(results)
 
# Save the results to an Excel file
results_df.to_excel('path', index=False)  # Adjust the file path as needed
