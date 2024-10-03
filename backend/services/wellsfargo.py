from utils.sleep import *

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

two_fa_sessions = {}

# TODO:
# add login
# add buy
# add account switching
# add multi buy function
def login(driver, tempdir, username, password):
    try:
        # Login logic
        username_field = WebDriverWait(driver,15).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="userid"]'))
        )
        human_type(username, username_field)
        very_short_sleep()

        pw_field = driver.find_element(By.XPATH, '//*[@id="password"]')
        human_type(password, pw_field)
        very_short_sleep()

        sign_on_button = driver.find_element(By.XPATH, '//*[@id="btnSignon"]')
        sign_on_button.click()

        send_mobile_2fa = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="app-modal-root"]/div[4]/div/div/div/div/div/div/div/div[2]/div/div[2]/div[2]/div/ul/li[1]/button'))
        )
        send_mobile_2fa.click()

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

def buy(tickers, dir, prof, trade_share_count, username, password, two_fa_code=None):
    driver, temp_dir = start_regular_driver(dir, prof)

    try:
        driver.get("https://www.wellsfargo.com/")
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

    enterTradeTicket(driver)    # Click on brokerage overview
    navigate_to_trade(driver)
    initiate_account_selection(driver)

    # In the trade ticket
    try:
        select_account_dropdown = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="dropdown2"]'))
        )
        select_account_dropdown.click()

        # Obtain number of accounts
        li_elements = driver.find_elements(By.CSS_SELECTOR, '#dropdownlist2 li')

        for account_num in li_elements:
            account_select = driver.find_element(By.XPATH, f'//*[@id="dropdownlist2"]/li[{account_num}]')
            account_select.click()

            try: 
                select_action = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '//*[@id="BuySellBtn"]'))
                )
                select_action.click()

                for ticker in tickers:
                    short_sleep()
                    order_url = driver.current_url

                    buy_action = driver.find_element(By.XPATH, '//*[@id="LOelALfK8Y"]')
                    # sell: //*[@id="eqentryfrm"]/div/div[1]/div[1]/div[1]/div[2]/ul/li[2]/a
                    buy_action.click()
                    very_short_sleep()

                    conduct_trade(driver, ticker, trade_share_count)
                    driver.get(order_url)
            except:
                print("Error configuring trade")
    except:
        print("Error occurred in trade ticket")

    print("No more accounts to process.")
    driver.quit()
    # handle_popup(driver)
    
def conduct_trade(driver, ticker, trade_share_count):
    ticker_input = driver.find_element(By.XPATH, '//*[@id="Symbol"]')
    human_type(ticker, ticker_input)
    very_short_sleep()

    share_qty = driver.find_element(By.XPATH, '//*[@id="OrderQuantity"]')
    human_type(trade_share_count, share_qty)
    very_short_sleep()

    order_type = driver.find_element(By.XPATH, '//*[@id="OrderTypeBtnText"]')
    order_type.click()

    limit_order = driver.find_element(By.XPATH, '//*[@id="ordertyperow"]/div[2]/div[2]/ul/li[1]/a')
    limit_order.click()
    very_short_sleep()

    current_price = driver.execute_script('document.querySelector("#prevdata > div.quoteestimate > div:nth-child(1) > div.qedata > div.qeval").textContent')
    current_price += 0.1  # Adjust for higher odds in order fill
    current_price = f"{current_price:.2f}"

    limit_input = driver.find_element(By.XPATH, '//*[@id="Price"]')
    human_type(current_price, limit_input)

    timing_select = driver.find_element(By.XPATH, '//*[@id="TIFBtnText"]')
    timing_select.click()

    day_select = driver.find_element(By.XPATH, '//*[@id="eqentryfrm"]/div/div[1]/div[5]/div/div[2]/div/ul/li[1]/a')
    day_select.click()

    preview_button = driver.find_element(By.XPATH, '//*[@id="actionbtnContinue"]')
    preview_button.click()

    try:
        submit_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="actionbtnbar"]/button[2]'))
        )
        submit_button.click()
    except:
        print("Error submitting order")
    very_short_sleep()


def navigate_to_trade(driver):
    try:
        brokerage_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="BROKERAGE_LINK7P"]'))
        )

        brokerage_button.click()
    except:
        print("Error clicking on brokerage tab")

def initiate_account_selection(driver):
    try:
        # Select Account
        portfolio_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="dropdown2"]'))
        )
        portfolio_button.click()
        very_short_sleep()

        trademenu_button =  WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="gotrading"]'))
        )
        trademenu_button.click()
    except:
        print("Error clicking on trade menu button")

def handle_popup(driver):
    try:
        # Continue if there is a popup
        popup_click_yes = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="btn-continue"]'))
        )
        popup_click_yes.click()
    except:
        print("No popup, continuing...")


def sell(tickers, dir, prof, trade_share_count, username, password, two_fa_code=None):
    driver, temp_dir = start_regular_driver(dir, prof)

    try:
        driver.get("https://www.wellsfargo.com/")
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
    enterTradeTicket(driver)    # Click on brokerage overview
    navigate_to_trade(driver)
    initiate_account_selection(driver)

    # In the trade ticket
    try:
        select_account_dropdown = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="dropdown2"]'))
        )
        select_account_dropdown.click()

        # Obtain number of accounts
        li_elements = driver.find_elements(By.CSS_SELECTOR, '#dropdownlist2 li')

        for account_num in li_elements:
            account_select = driver.find_element(By.XPATH, f'//*[@id="dropdownlist2"]/li[{account_num}]')
            account_select.click()

            try: 
                select_action = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '//*[@id="BuySellBtn"]'))
                )
                select_action.click()

                for ticker in tickers:
                    short_sleep()
                    order_url = driver.current_url

                    sell_action = driver.find_element(By.XPATH, '//*[@id="eqentryfrm"]/div/div[1]/div[1]/div[1]/div[2]/ul/li[2]/a')
                    sell_action.click()
                    very_short_sleep()

                    conduct_trade(driver, ticker, trade_share_count)
                    driver.get(order_url)
            except:
                print("Error configuring trade")
    except:
        print("Error occurred in trade ticket")

    print("No more accounts to process.")
    driver.quit()
    # handle_popup(driver)

def enterTradeTicket(driver):
    try:
        print("Initiating buy...")
        portfolio_tab = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="MrA7JYMdjr"]/a'))
        )
        portfolio_tab.click()

        trade_tab = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="gotrading"]'))
        )
        trade_tab.click()
    except:
        print("Error entering trade ticket")

def complete_2fa_and_trade(session_id, two_fa_code=None):
    logger.info(f"Completing 2FA for Wells Fargo session {session_id}.")

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
    # username = session_info.get('username')
    # password = session_info.get('password')

    try:
        verify_code = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="otp"]'))
        )
        human_type(two_fa_code, verify_code)
        very_short_sleep()

        continue_button = driver.find_element(By.XPATH, '//*[@id="FWNKNNFK"]')
        continue_button.click()
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