from utils.sleep import *

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

two_fa_sessions = {}

# TODO:
# add 2FA handling
# add multi buy function
def buy(tickers, dir, prof, trade_share_count, username, password, two_fa_code=None):
    driver, temp_dir = start_regular_driver(dir, prof)

    try:
        driver.get("https://invest.firstrade.com/cgi-bin/login")
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
    except:
        print("Error logging in")


def buy_after_login(driver, tickers, trade_share_count):
    try:
        account_dropdown = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="head"]/ul/li[7]/div'))
        )
        account_dropdown.click()
        short_sleep()
        accounts_column = driver.find_elements(By.XPATH, '//*[@id="headcontent"]/div[3]/div[2]/table/tbody//a')
    except:
        print("Error finding number of accounts...")

    bought_accounts = set()
    for account in range(1, len(accounts_column) + 1):
        if account != 1:
            setup_trade(driver)

        current_account = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, f'//*[@id="headcontent"]/div[3]/div[2]/table/tbody/tr[{account}]/th/a'))
        )
        bought_accounts.add(current_account.text)
        current_account.click()
        
        for ticker in tickers:
            ticker_search(driver, ticker)
            logger.info("\n\n\n\nBuying " + ticker+"\n\n\n")

            # buy button
            try:
                buy_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '//*[@id="maincontent"]/div/div[2]/div[1]/div[3]/button[1]'))
                )
                buy_button.click()
                short_sleep()
            except:
                print("\n\nError in clicking buy button...\n\n")

            enter_qty(driver, trade_share_count)
            submit_order(driver)
        
    print("No more accounts to process.")
    driver.quit()


def sell(tickers, dir, prof, trade_share_count, username, password, two_fa_code=None):
    driver, temp_dir = start_regular_driver(dir, prof)

    try:
        driver.get("https://invest.firstrade.com/cgi-bin/login")
        login_response = login(driver, temp_dir, username, password)
        
        if login_response['status'] == '2FA_required':
            logger.info(f"2FA required via {login_response['method']}.")
            # Store action details in the session
            session_id = login_response.get('session_id')
            two_fa_sessions[session_id]['action'] = 'sell'
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
            # Proceed with selling
            trade_response = sell_after_login(driver, tickers, trade_share_count)
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
        logger.error(f"Error during sell operation: {str(e)}")
        driver.quit()
        shutil.rmtree(temp_dir, ignore_errors=True)
        return {
            'status': 'failure',
            'message': f'Failed to sell {tickers}.',
            'error': str(e)
        }
    except:
        print("Error logging in")

def sell_after_login(driver, tickers, trade_share_count):
    try:
        account_dropdown = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="head"]/ul/li[7]/div'))
        )
        account_dropdown.click()
        short_sleep()
        accounts_column = driver.find_elements(By.XPATH, '//*[@id="headcontent"]/div[3]/div[2]/table/tbody//a')
    except:
        print("Error finding number of accounts...")

    sold_accounts = set()
    for account in range(1, len(accounts_column) + 1):
        if account != 1:
            setup_trade(driver)

        current_account = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, f'//*[@id="headcontent"]/div[3]/div[2]/table/tbody/tr[{account}]/th/a'))
        )
        sold_accounts.add(current_account.text)
        current_account.click()

        for ticker in tickers:
            ticker_search(driver, ticker)

            # sell button
            try:
                sell_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '//*[@id="maincontent"]/div/div[2]/div[1]/div[3]/button[2]'))
                )
                sell_button.click()
                short_sleep()
            except:
                print("\n\nError in clicking buy button...\n\n")

            enter_qty(driver, trade_share_count)
            submit_order(driver)
        
    print("No more accounts to process.")
    driver.quit()


# login and 2FA handling
def login(driver, tempdir ,username, password):
    try:
        username_field = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="username"]'))
        )
        username_field.click()
        human_type(username, username_field)

        pw_field = driver.find_element(By.XPATH, '//*[@id="password"]')
        human_type(password, pw_field)
        short_sleep()

        submit_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="loginButton"]'))
        )
        submit_button.click()

        send_by_text = WebDriverWait(driver, 24).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="form-recipients"]/label[2]/div/div[1]/input'))
        )
        send_by_text.click()
        send_code = WebDriverWait(driver, 24).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="send-code"]'))
        )
        send_code.click()

        # Generate a unique session ID
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
    except:
        print("2FA not required. Login successful.")
        return {'status': 'success'}

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
        # Enter and submit the 2FA code
        verify_code = WebDriverWait(driver, 25).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="code"]'))
        )

        human_type(two_fa_code, verify_code)

        submit_code = driver.find_element(By.XPATH, '//*[@id="verify-code"]')
        submit_code.click()
        WebDriverWait(driver, 10).until(
            EC.url_to_be('https://invest.firstrade.com/cgi-bin/main#/cgi-bin/home')
        )
        logger.info("Logged into First Trade!")
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


# gets the number of accounts needed to iterate through
def get_num_accounts(driver):
    try:
        account_dropdown = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="head"]/ul/li[7]/div'))
        )
        account_dropdown.click()
        very_short_sleep()
        accounts_column = driver.find_element(By.XPATH, '//*[@id="headcontent"]/div[3]/div[2]/table/tbody//a')
        return accounts_column
    except:
        print("Error finding number of accounts...")

# sets up trade by inputting ticker and searching
def setup_trade(driver):
    try:
        account_dropdown = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="head"]/ul/li[7]/div'))
        )
        account_dropdown.click()
        short_sleep()
    except:
        print("\n\nError in clicking dropdown...\n\n")


def ticker_search(driver, ticker):
    try:

        print("\n\n\n" + ticker + "\n\n\n")
        # input ticker
        t_search = driver.find_element(By.XPATH, '//*[@id="id-symlookup"]')
        t_search.clear()
        very_short_sleep()
        human_type(ticker, t_search)
        very_short_sleep()

        # click on search
        t_search = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="id-searchbtngo"]'))
        )
        t_search.click()
        short_sleep()
    except:
        print("\n\nError in setting up trade...\n\n")

# enters the quantity
def enter_qty(driver, qty):
    # qty
    try:
        share_qty = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="quantity"]'))
        )
        share_qty.send_keys(Keys.CLEAR)
        human_type("1", share_qty)
    except:
        print("\n\nError in entering the quantity...\n\n")

# submits the trade
def submit_order(driver):
    # send order (submit)
    try:
        send_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="submitOrder"]'))
        )
        send_button.click()
        short_sleep()
    except:
        print("\n\nError in submitting order...\n\n")