from utils.sleep import *
import tkinter as tk
from tkinter import messagebox
# TODO:
# add login
# add buy
# add account switching
# add multi buy function

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

two_fa_sessions = {}
def buy(tickers, dir, prof, trade_share_count, username, password, two_fa_code=None):
    driver, temp_dir = start_regular_driver(dir, prof)

    try:
        driver.get("https://app.webull.com/watch")
        login_response = login(driver, temp_dir, username, password)
        
        if login_response['status'] == '2FA_required':
            logger.info(f"2FA required via {login_response['method']}.")
            # Store action details in the session
            session_id = login_response.get('session_id')
            two_fa_sessions[session_id]['action'] = 'buy'
            two_fa_sessions[session_id]['tickers'] = tickers
            two_fa_sessions[session_id]['trade_share_count'] = trade_share_count
            os.system('echo \a')
            return {
                'status': '2FA_required',
                'method': login_response['method'],
                'session_id': session_id,
                'message': '2FA is required'
            }
        elif login_response['status'] == 'success':
            # Proceed with buying
            trade_response = buy_after_login(driver, tickers, trade_share_count)
            driver.quit()
            shutil.rmtree(temp_dir, ignore_errors=True)
            return trade_response

        else:
            # Handle other statuses
            driver.quit()
            shutil.rmtree(temp_dir, ignore_errors=True)
            return {
                'status': 'failure',
                'message': login_response.get('message', 'Login failed.')
            }
    except Exception as e:
        logger.error(f"Error during buy operation: {str(e)}")
        driver.quit()
        shutil.rmtree(temp_dir, ignore_errors=True)
        return {
            'status': 'failure',
            'message': f'Failed to buy {tickers}.',
            'error': str(e)
        }
    
def buy_after_login(driver, tickers, trade_share_count):
    try:
        ticker_search = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="app"]/div/form/span/div/span/input'))
        )
        
    except:
        pass
    
def login(driver, tempdir, username, password):
    try:
        # Close popup
        exit_popup = WebDriverWait(driver, 6).until(
            EC.element_to_be_clickable((By.XPATH, '/html/body/div[5]/div/div/div/i'))
        )
        exit_popup.click()

        exit_panel_popup = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, '/html/body/div[5]/div/div/div[2]/i'))
        )
        exit_panel_popup.click()

        very_short_sleep()
        driver.execute_script("document.elementFromPoint(window.innerWidth/2, 0).click();")
    except:
        print("No popup found")
    
    try:
        login_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="app"]/div/div[1]/div[2]/span'))
        )
        login_button.click()

        phoneNum_field = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '/html/body/div[5]/div/div/div/div[2]/div[2]/div[2]/div/span/input'))
        )
        human_type(username, phoneNum_field)
        very_short_sleep()

        pw_field = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '/html/body/div[5]/div/div/div/div[2]/div[2]/div[3]/div/div/span/input'))
        )
        human_type(password, pw_field)
        very_short_sleep()

        login_button = driver.find_element(By.XPATH, '/html/body/div[5]/div/div/div/div[2]/div[2]/button')
        login_button.click()

        if is_captcha_present(driver):
            logger.info("Captcha detected.")
            # Generate a unique session ID
            session_id = str(uuid.uuid4())
            two_fa_sessions[session_id] = {
                'driver': driver,
                'temp_dir': tempdir,  # Store temp_dir for cleanup
                'username': username,
                'password': password,
                'method': 'captcha_and_text',  # Indicate both Captcha and 2FA are needed
                'action': None  # To be set by buy/sell functions
            }
            return {
                'status': '2FA_required',
                'method': 'captcha_and_text',
                'session_id': session_id,
                'message': 'Captcha and 2FA are required. Please solve the Captcha and enter your 2FA code.'
            }

        # Proceed with 2FA if no captcha
        session_id = str(uuid.uuid4())
        two_fa_sessions[session_id] = {
            'driver': driver,
            'temp_dir': tempdir,  # Store temp_dir for cleanup
            'username': username,
            'password': password,
            'method': 'text',
            'action': None  # To be set by buy/sell functions
        }

        return {'status': '2FA_required', 'method': 'text', 'session_id': session_id}

    except Exception as e:
        print(f"An error occurred during login: {e}")

def is_captcha_present(driver):
    try:
        WebDriverWait(driver, 10).until(lambda driver: driver.execute_script('return document.readyState') == 'complete')

        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "/html/body/div[7]/div/div/div"))
        )
        os.system('echo \a')
        very_short_sleep()
        os.system('echo \a')
        return True
    except:
        return False
    
def prompt_user_to_solve_captcha():
    return {
        'status': 'captcha_required',
        'message': 'Captcha is required. Please solve it in the browser.'
    }

def complete_2fa_and_trade(session_id, two_fa_code=None):
    logger.info(f"Completing 2FA for session {session_id}.")

    if not two_fa_code:
        logger.error("2FA code is missing for text-based 2FA.")
        return {'status': 'error', 'message': '2FA code is required for text-based 2FA.'}

    if session_id not in two_fa_sessions:
        logger.error("Invalid session ID.")
        return {'status': 'error', 'message': 'Invalid session ID.'}

    session_info = two_fa_sessions[session_id]
    driver = session_info['driver']
    temp_dir = session_info['temp_dir']
    # method = session_info['method'] # Only has 'text' method 
    action = session_info['action']
    tickers = session_info.get('tickers')
    # ticker = session_info.get('ticker')
    trade_share_count = session_info.get('trade_share_count')
    username = session_info.get('username')
    password = session_info.get('password')

    try:
        WebDriverWait(driver, 10).until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
        element = driver.find_element(By.XPATH, '/html/body/div[5]/div/div/div/div[2]/div[3]/div/span/input')
        # element = driver.find_element(By.CSS_SELECTOR, "#app > div > div.csr6 > div > div > div > div > div[class^='csr'] > div > div > input")
        human_type(two_fa_code, element)

        submit_code = driver.find_element(By.XPATH, '/html/body/div[5]/div/div/div/div[2]/div[4]/button')
        submit_code.click()

        WebDriverWait(driver, 10).until(
            EC.url_to_be('https://www.webull.com/center')
        )
        logger.info("Logged into Webull!")
    except:
        print("Error completing 2FA")
        return {'status': 'error', 'message': '2FA was incorrect.'}
    
    short_sleep()
    # After 2FA, proceed with the trade
    if action == 'buy':
        trade_response = buy_after_login(driver, tickers, trade_share_count)
    # elif action == 'sell':
    #     trade_response = sell_after_login(driver, tickers, trade_share_count)
    else:
        logger.error("Invalid trade action specified.")
        return {'status': 'error', 'message': 'Invalid trade action specified.'}

    # Clean up
    driver.quit()
    shutil.rmtree(temp_dir, ignore_errors=True)
    del two_fa_sessions[session_id]

    return trade_response