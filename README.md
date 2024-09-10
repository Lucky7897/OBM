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

The `accounts.txt` file (or `qccount.txt` as you referred to it) is used to store credentials in a structured format for the script to read. Here’s how you might structure it based on your script’s requirements:

### Format

Each line in `accounts.txt` should represent a single account with the following format:

```
login_url:username:password
```

### Example

Here’s a sample `accounts.txt` file:

```
https://example.com/login:myusername:mypassword
https://anotherexample.com/signin:anotheruser:anotherpassword
```

### Creating and Using `accounts.txt`

1. **Create the File:**
   - Open a text editor.
   - Enter the credentials in the format shown above.
   - Save the file as `accounts.txt`.

2. **Add `accounts.txt` to Your Project Directory:**
   Place the `accounts.txt` file in the root directory of your project or a directory where your script can access it.

3. **Update Your Script (if needed):**
   Ensure that your script correctly loads and processes this file. For example, your script should be able to handle each line, split it into `login_url`, `username`, and `password`, and use these values to perform login operations.

### Example Directory Layout Including `accounts.txt`

```
OBM/
├── autoconfigmaker.py           # Your main script
├── requirements.txt             # File listing the required Python packages
├── README.md                    # Project documentation
├── LICENSE                      # License file (if applicable)
├── .gitignore                   # Git ignore file (optional)
└── accounts.txt                 # File containing login credentials
```

### Example of Loading Accounts in the Script

Here’s how you might modify the `load_accounts_from_file` function to read from `accounts.txt`:

```python
def load_accounts_from_file():
    """Load account credentials from a local text file."""
    file_path = 'accounts.txt'
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"{file_path} not found.")
    
    with open(file_path, 'r') as file:
        accounts = file.readlines()
    
    return [line.strip().split(':') for line in accounts if line.strip()]
```

This function reads the `accounts.txt` file, splits each line into `login_url`, `username`, and `password`, and returns a list of these values.

Make sure to include this file in your Git repository if you want others to have access to it. If it contains sensitive information, consider using `.gitignore` to exclude it from version control or ensure it’s only available in a secure manner.

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
