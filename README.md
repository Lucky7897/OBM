```markdown
# **OpenBullet Configuration Automation Script**

This script automates the process of generating an OpenBullet configuration file by extracting form details from a login page, performing login operations using provided credentials, and generating an OpenBullet configuration file based on the extracted parameters.

## **Requirements**

- **Python 3.x**
- **Playwright**: Install using:
  ```bash
  pip install playwright
  ```
- **Playwright Browsers**: Install using:
  ```bash
  playwright install
  ```

## **Installation**

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/Lucky7897/OBM.git
   cd OBM
   ```

2. **Install Dependencies:**
   ```bash
   pip install playwright
   playwright install
   ```

3. **Save the Script:**
   Save the script as `autoconfigmaker.py` in your local repository.

## **Script Components**

### **Functions:**

- `random_delay(min_ms, max_ms, debug_mode=False)`:  
  Introduces a random delay or a fixed delay in debug mode.

- `take_screenshot(page, step, debug_mode)`:  
  Takes a screenshot of the current page if debug mode is enabled.

- `confirm_selector(page, element_type, default_selector)`:  
  Allows manual confirmation or correction of CSS selectors for elements.

- `extract_form_details(page)`:  
  Extracts form action URL, method, and input fields from the page.

- `perform_login(page, action_url, method, parameters, username, password, debug_mode, debug_plus_mode)`:  
  Performs the login operation and handles different input types.

- `generate_openbullet_config(action_url, parameters, headers, incomplete=False)`:  
  Generates an OpenBullet configuration file based on extracted parameters.

- `load_accounts_from_file()`:  
  Loads account credentials from a selected text file.

- `automate_openbullet_config(debug_mode=False, debug_plus_mode=False)`:  
  Main function to automate the process of extracting parameters and generating the configuration.

## **Running the Script**

### **Command Line Execution:**

1. Open a terminal or command prompt.
2. Navigate to the directory where `autoconfigmaker.py` is saved.
3. Run the script with:
   ```bash
   python autoconfigmaker.py
   ```

### **Follow the Prompts:**

- **Enable Debug Mode?**: Input `y` or `n` to enable or disable debug mode.
- **Enable Debug Plus Mode?**: Input `y` or `n` to enable or disable debug plus mode.
- **Select Credential Source**:
  - **Local TXT File**: Choose a text file with credentials.
  - **Manual Entry**: Input login URL, username, and password manually.

## **Text File Format**

- **Account Entries**: Each line should have the format `login_url:username:password`.

  Example:
  ```txt
  https://example.com/login:myusername:mypassword
  ```

## **Debug and Debug Plus Modes**

- **Debug Mode**: Takes screenshots and introduces delays to help with debugging.
- **Debug Plus Mode**: Includes additional prompts to handle interactive elements (e.g., consent checkboxes).

## **Configuration File Output**

### **Generated Files**:
- `openbullet_config.json`: Complete configuration file.
- `openbullet_config_incomplete.json`: Incomplete configuration file if any fields are missing.

## **Error Handling**

- **Error Logging**: Any issues encountered during execution will be logged.
- **Screenshots**: Captures screenshots of the page at various stages if debug mode is enabled.

## **Troubleshooting**

- **Invalid Account Format**: Ensure each line in the credentials file follows the correct format.
- **Element Not Found**: Verify that the CSS selectors for elements are accurate.
- **Login Issues**: Confirm the login URL and credentials are correct.

## **License**

This project is licensed under the MIT License - see the LICENSE file for details.

## **Contact**

For additional support or questions, you may need to consult the documentation of the libraries used or seek help from online communities related to Playwright or web scraping.
```
