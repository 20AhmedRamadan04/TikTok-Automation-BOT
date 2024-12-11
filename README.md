# TikTok-Automation-BOT 🚀  

## Overview  
**TikTok-Automation-BOT** is a Python-based script designed to streamline TikTok account management by automating:  
- Login processes for multiple accounts.  
- Profile data extraction (e.g., followers, coin balances).  
- Managing successful and failed account logins.  

The bot leverages **Selenium** for browser automation and integrates with a CAPTCHA-solving API for bypassing challenges.

---

## Features 🌟  
- **Automated TikTok login** for multiple accounts.  
- **CAPTCHA-solving** integration using an external API.  
- **Profile data extraction**: Followers count, coin balance, and username.  
- **Error management**: Differentiates successful and failed logins for better oversight.  

---

## Prerequisites 🛠️  

### Required Software  
- **Python 3.x**: Version 3.8 or higher is recommended.  
- **Google Chrome**: Required for browser automation.  
- **ChromeDriver**: Ensure it matches your Chrome version. [Download ChromeDriver here](https://sites.google.com/chromium.org/driver/).  

### Required Python Modules  
Install all dependencies using pip:  
```bash  
pip install selenium undetected-chromedriver beautifulsoup4 phonenumbers colorama fake_useragent  
```  

---

## Setup ⚙️  

### 1. Prepare `data.txt`  
Create a file named `data.txt` in the project directory with account details in the following format:  
```  
+1234567890:password123  
```  
Each line represents an account with a phone number (or email) and password.

### 2. CAPTCHA API Key  
Replace the placeholder in the script with your CAPTCHA-solving API key:  
```python  
self.api_key = 'YOUR_CAPTCHA_API_KEY'  # Replace with your API key  
```  

### 3. Configuration  
Ensure ChromeDriver is in your system's `PATH` or provide its full path in the script.

---

## Usage 🚀  

Run the script using the following command:  
```bash  
python main.py  
```  

The bot will:  
1. Read accounts from `data.txt`.  
2. Log in to each account.  
3. Extract profile data (username, followers, coins) for successful logins.  
4. Save results to `result.txt` and log failed accounts in `corrupted_accounts.txt`.  

---

## Files Created During Execution 📂  
- **`result.txt`**: Stores data for successful logins.  
- **`corrupted_accounts.txt`**: Logs credentials of accounts that failed to log in.  

---

## Notes 📝  
- Ensure `data.txt` contains valid credentials.  
- Use a trusted CAPTCHA API service and safeguard your API key.  
- This script is designed for **educational purposes only**. Misuse may violate TikTok's terms of service.  

---

## Disclaimer ⚠️  
This tool is for **educational purposes only**. The author is not liable for misuse. Please adhere to TikTok's terms of service and applicable laws.

---

How does this look? Let me know if you'd like further tweaks! 😊
