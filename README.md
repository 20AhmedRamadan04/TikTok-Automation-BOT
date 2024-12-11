TikTok-Automation-BOT

Overview

TikTok-Automation-BOT is a Python script designed to automate TikTok account login, extract profile data (such as followers and coin balances), and handle multiple accounts. The bot uses Selenium for browser automation and integrates with a CAPTCHA-solving API for bypassing challenges.

Features

Automated TikTok login for multiple accounts.

CAPTCHA-solving integration using an external API.

Extraction of profile data, including followers count and coin balance.

Management of successful and failed account logins.

Prerequisites

Required Software

Python 3.x: Make sure you have Python 3.8 or higher installed.

Google Chrome: The bot uses Chrome for automation.

ChromeDriver: Ensure ChromeDriver matches your Chrome version. You can download it from here: https://sites.google.com/chromium.org/driver/.

Required Python Modules

Install the required dependencies using pip:
pip install required_module_name
Modules included:

selenium

undetected-chromedriver

beautifulsoup4

phonenumbers

colorama

fake_useragent

Setup

1. Prepare data.txt

Create a file named data.txt in the project directory. Add your accounts in the format:
+1234567890:password123
Each line represents an account with a phone number or email and password.

2. CAPTCHA API Key

The script uses a CAPTCHA-solving API. Replace the placeholder in the script with your API key:
self.api_key = 'YOUR_CAPTCHA_API_KEY'  # Replace with your API key
3. Configuration

Ensure ChromeDriver is in your PATH or provide the path in the script.

Usage

To run the script, use the following command:
python main.py
The bot will:

Read accounts from data.txt.

Attempt to log in to each account.

Extract profile data (username, followers, coins) for successful logins.

Save results to result.txt and failed logins to corrupted_accounts.txt.

Files Created During Execution

result.txt: Stores data for successful logins.

corrupted_accounts.txt: Stores credentials of accounts that failed to log in.

Notes

Ensure data.txt contains valid credentials.

Use a secure CAPTCHA API service and keep your API key private.

The script is designed for educational purposes only. Unauthorized use of the bot may violate TikTok’s terms of service.

Disclaimer

This tool is provided for educational purposes only. The author is not responsible for any misuse of the script. Please use it responsibly and in compliance with applicable laws.
