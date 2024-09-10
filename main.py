from playwright.sync_api import sync_playwright
import json
import logging
from urllib.parse import urlencode
import time
import os

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

def random_delay(min_ms, max_ms, debug_mode=False):
    """Pause the execution for a random duration between min_ms and max_ms milliseconds."""
    if debug_mode:
        time.sleep(5)  # Always wait 5 seconds in debug mode
    else:
        delay = (min_ms + (max_ms - min_ms) * 0.001)
        time.sleep(delay)

def take_screenshot(page, step, debug_mode):
    """Take a screenshot of the page if debug mode is enabled."""
    if debug_mode:
        page.screenshot(path=f'screenshot_{step}.png')
        logging.info(f'Screenshot taken for step: {step}')

def confirm_selector(page, element_type, default_selector):
    """Confirm the selector for an element in debug plus mode."""
    logging.info(f"Captured {element_type} element with selector: {default_selector}")
    is_correct = input(f"Is this selector for {element_type} correct? (y/n): ").strip().lower()

    if is_correct == 'n':
        return input(f"Please enter the correct CSS selector for the {element_type}: ").strip()
    return default_selector

def extract_form_details(page):
    """Extract form details including action URL, input fields, and their types."""
    form = page.query_selector('form')
    if not form:
        logging.error("No form found on the login page.")
        raise Exception("No form found on the login page.")

    action_url = form.get_attribute('action') or page.url
    method = form.get_attribute('method') or 'get'
    inputs = form.query_selector_all('input')
    textareas = form.query_selector_all('textarea')
    selects = form.query_selector_all('select')

    parameters = {}
    for input_tag in inputs:
        name = input_tag.get_attribute('name')
        type_ = input_tag.get_attribute('type') or 'text'
        if name:
            parameters[name] = type_

    for textarea in textareas:
        name = textarea.get_attribute('name')
        if name:
            parameters[name] = 'textarea'

    for select in selects:
        name = select.get_attribute('name')
        if name:
            parameters[name] = 'select'

    if not parameters:
        logging.error("No recognizable form fields found.")
        raise Exception("No recognizable form fields found.")

    logging.info(f'Extracted form action URL: {action_url}')
    logging.info(f'Form method: {method}')
    logging.info(f'Login parameters: {parameters}')

    return action_url, method, parameters

def perform_login(page, action_url, method, parameters, username, password, debug_mode, debug_plus_mode):
    """Perform the login and handle different input types."""
    if debug_plus_mode:
        # Automatically detect elements and ask for confirmation
        email_selector = page.locator('input[type="email"], input[name="email"], input[id*="email"]').first.evaluate('this.getAttribute("id")')
        password_selector = page.locator('input[type="password"], input[name="password"], input[id*="password"]').first.evaluate('this.getAttribute("id")')

        email_selector = confirm_selector(page, 'email', email_selector)
        password_selector = confirm_selector(page, 'password', password_selector)
    else:
        # Use default selectors based on provided HTML
        email_selector = 'input[name="email"]'
        password_selector = 'input[name="password"]'

    # Record user interactions for debug_plus_mode
    if debug_plus_mode:
        page.on('click', lambda e: logging.info(f'User clicked on: {e.target}'))

    # Fill in the email and password fields
    page.fill(email_selector, username)
    page.fill(password_selector, password)
    take_screenshot(page, 'form_filled', debug_mode)

    # Perform login by submitting the form
    if method.upper() == 'POST':
        with page.expect_navigation():
            page.evaluate("document.querySelector('form').submit()")
    else:  # For GET method
        query_string = urlencode(parameters)
        url_with_params = f"{action_url}?{query_string}"
        page.goto(url_with_params)
        take_screenshot(page, 'after_get_request', debug_mode)

    # Capture response content
    response = page.content()
    logging.info(f'Response content after login: {response[:500]}')  # Log first 500 chars of the response

    return response

def generate_openbullet_config(action_url, parameters, headers, incomplete=False):
    """Generate an OpenBullet configuration file based on the extracted parameters."""
    body = "&".join(f"{key}={{ {key} }}" for key in parameters.keys())
    filename = 'openbullet_config_incomplete.json' if incomplete else 'openbullet_config.json'

    config = {
        "SETTINGS": {
            "Name": "Generated Config",
            "SuggestedBots": 100,
            "MaxCPM": 0,
            "LastModified": time.strftime('%Y-%m-%dT%H:%M:%S'),
            "Author": "Grimoire",
            "NeedsProxies": True,
            "MaxRedirects": 8
        },
        "REQUESTS": [
            {
                "name": "Login",
                "url": action_url,
                "method": "POST",
                "headers": headers,
                "body": body
            }
        ]
    }

    with open(filename, 'w') as f:
        json.dump(config, f, indent=4)
    status = 'INCOMPLETE' if incomplete else 'COMPLETE'
    logging.info(f'OpenBullet configuration file ({status}) generated: {filename}')

def load_accounts_from_file():
    """Load account credentials from a local text file."""
    files = [f for f in os.listdir() if f.endswith('.txt')]
    print("Available text files:")
    for i, file in enumerate(files, 1):
        print(f"{i}: {file}")
    
    choice = int(input("Select the file by number: ").strip())
    if 1 <= choice <= len(files):
        file_path = files[choice - 1]
        with open(file_path, 'r') as file:
            accounts = file.readlines()
        return [line.strip().split(':') for line in accounts]
    else:
        raise ValueError("Invalid file selection.")

def automate_openbullet_config(debug_mode=False, debug_plus_mode=False):
    """Automate the entire process from parameter extraction to configuration file generation."""
    use_file = input('Do you want to select a local txt file with credentials? (y/n): ').strip().lower() == 'y'

    if use_file:
        accounts = load_accounts_from_file()
    else:
        login_url = input('Enter the login URL: ').strip()
        username = input('Enter the username: ').strip()
        password = input('Enter the password: ').strip()
        accounts = [(login_url, username, password)]

    for i, account in enumerate(accounts[:10]):  # Limit to 10 accounts
        if len(account) == 3:
            login_url, username, password = account
        elif len(account) == 2:
            login_url, username = account
            password = input(f"Enter the password for {username}: ").strip()
        else:
            logging.error(f'Invalid account format: {account}')
            continue

        logging.info(f'Processing account {i + 1}: {username}')
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=not debug_mode)
            page = browser.new_page()
            page.goto(login_url)
            take_screenshot(page, 'initial_load', debug_mode)

            try:
                if debug_plus_mode:
                    checkbox_prompt = input('Did the site include any checkboxes (like "I agree" or consent)? (y/n): ').strip().lower()
                    if checkbox_prompt == 'y':
                        legal_age_selector = input('Enter the selector for legal age checkbox: ').strip()
                        privacy_selector = input('Enter the selector for privacy checkbox: ').strip()
                        cookies_selector = input('Enter the selector for cookies checkbox: ').strip()
                        accept_button_selector = input('Enter the selector for the ACCEPT button: ').strip()
                        
                        # Consent checkboxes
                        logging.info('Checking consent checkboxes')
                        page.locator(legal_age_selector).check()
                        random_delay(1000, 2000, debug_mode)
                        page.locator(privacy_selector).check()
                        random_delay(1000, 2000, debug_mode)
                        page.locator(cookies_selector).check()
                        random_delay(1000, 2000, debug_mode)
                        take_screenshot(page, 'consent_checkboxes_checked', debug_mode)

                        # Click ACCEPT button
                        logging.info('Clicking the ACCEPT button')
                        page.locator(accept_button_selector).click()
                        random_delay(2000, 3000, debug_mode)
                        take_screenshot(page, 'accept_button_clicked', debug_mode)

                # Extract form details and perform login
                action_url, method, parameters = extract_form_details(page)
                response = perform_login(page, action_url, method, parameters, username, password, debug_mode, debug_plus_mode)

                # Prepare headers for OpenBullet config
                headers = {
                    "Content-Type": "application/x-www-form-urlencoded",
                    "User-Agent": page.evaluate("navigator.userAgent")
                }

                # Check if login was successful and generate OpenBullet config
                if 'dashboard' in response.lower() or 'welcome' in response.lower():
                    logging.info(f'Login successful for {username}')
                    generate_openbullet_config(action_url, parameters, headers)
                else:
                    logging.error(f'Login failed for {username}')

            except Exception as e:
                logging.error(f'An error occurred for {username}: {e}')
                take_screenshot(page, 'error_occurred', debug_mode)
            
            finally:
                browser.close()

if __name__ == '__main__':
    debug_mode = input('Enable debug mode? (y/n): ').strip().lower() == 'y'
    debug_plus_mode = input('Enable debug plus mode? (y/n): ').strip().lower() == 'y'
    automate_openbullet_config(debug_mode, debug_plus_mode)
