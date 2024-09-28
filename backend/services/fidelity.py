from utils.sleep import *

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

two_fa_sessions = {}

def login(driver, tempdir ,username, password):
    short_sleep()
    wait = WebDriverWait(driver, 24)
    try:
        # Enter username
        username_field = driver.find_element(By.XPATH, '//*[@id="dom-username-input"]')
        username_field.click()
        human_type(username, username_field)
        short_sleep()

        # Enter password
        pw_field = driver.find_element(By.XPATH, '//*[@id="dom-pswd-input"]')
        human_type(password, pw_field)
        short_sleep()

        logger.info("Clicking login button.")
        log_in_button = driver.find_element(By.XPATH, '//*[@id="dom-login-button"]')
        log_in_button.click()

        # Attempt to detect 2FA
        try:
            # Check for "Don't ask again" checkbox indicating 2FA is present
            dont_ask_again_button = wait.until(
                EC.element_to_be_clickable((
                    By.XPATH, '//*[@id="dom-widget"]/div/div[2]/pvd-field-group/s-root/div/div/s-slot/s-assigned-wrapper/pvd-form/s-root/div/form/s-slot/s-assigned-wrapper/div[1]/div/div/pvd-field-group/s-root/div/div/s-slot/s-assigned-wrapper/pvd-checkbox/s-root/div/label'))
            )

            logger.info("Detected 2FA requirement.")

            # Click "Don't ask again" to proceed
            dont_ask_again_button.click()
            very_short_sleep()

            # Attempt 2FA via Text
            try:
                send_as_text = wait.until(
                    EC.element_to_be_clickable((
                        By.XPATH, '//*[@id="dom-try-another-way-link"]'))
                )
                send_as_text.click()

                logger.info("Attempting to send 2FA code via text.")
                text_code_button = wait.until(
                    EC.element_to_be_clickable((
                        By.XPATH, '//*[@id="dom-channel-list-primary-button"]'))
                )
                text_code_button.click()
                very_short_sleep()

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

                # Indicate that Text-Based 2FA is required
                return {'status': '2FA_required', 'method': 'text', 'session_id': session_id}

            except TimeoutException:
                logger.warning("Text-Based 2FA not available. Trying App Notification.")

                # Attempt 2FA via App Notification
                try:
                    send_2fa_button = wait.until(
                        EC.element_to_be_clickable((
                            By.XPATH, '//*[@id="dom-push-primary-button"]'))
                    )
                    send_2fa_button.click()
                    logger.info("Sent 2FA request via app notification.")

                    # Generate a unique session ID
                    session_id = str(uuid.uuid4())
                    two_fa_sessions[session_id] = {
                        'driver': driver,
                        'temp_dir': tempdir,
                        'username': username,
                        'password': password,
                        'method': 'app',
                        'action': None  # To be set by buy/sell functions
                    }

                    # Indicate that App Notification-Based 2FA is required
                    return {'status': '2FA_required', 'method': 'app', 'session_id': session_id}

                except TimeoutException:
                    logger.error("Failed to initiate 2FA via both Text and App.")
                    return {'status': 'error', 'message': 'Failed to initiate 2FA.'}

        except TimeoutException:
            logger.info("2FA not required. Login successful.")
            save_cookies(driver, "f_cookies.pkl")
            short_sleep()
            return {'status': 'success'}

    except Exception as e:
        logger.error(f"Error during login: {str(e)}")
        raise e



def complete_2fa_and_trade(session_id, two_fa_code=None):
    """
    Completes the 2FA process based on the session ID and performs the trade.
    """
    logger.info(f"Completing 2FA for session {session_id}.")

    if session_id not in two_fa_sessions:
        logger.error("Invalid session ID.")
        return {'status': 'error', 'message': 'Invalid session ID.'}

    session_info = two_fa_sessions[session_id]
    driver = session_info['driver']
    temp_dir = session_info['temp_dir']
    method = session_info['method']
    action = session_info['action']
    tickers = session_info.get('tickers')
    ticker = session_info.get('ticker')
    trade_share_count = session_info.get('trade_share_count')
    username = session_info.get('username')
    password = session_info.get('password')

    try:
        wait = WebDriverWait(driver, 24)
        if method == 'text':
            if not two_fa_code:
                logger.error("2FA code is missing for text-based 2FA.")
                return {'status': 'error', 'message': '2FA code is required for text-based 2FA.'}

            # Enter the 2FA code received via text
            code_input = wait.until(
                EC.element_to_be_clickable((
                    By.XPATH, '//*[@id="dom-otp-code-input"]'))
            )
            human_type(two_fa_code, code_input)

            asking_again = wait.until(
                EC.element_to_be_clickable((
                    By.XPATH, '//*[@id="dom-widget"]/div/div[2]/pvd-field-group/s-root/div/div/s-slot/s-assigned-wrapper/pvd-form/s-root/div/form/s-slot/s-assigned-wrapper/div[1]/pvd-field-group/s-root/div/div/s-slot/s-assigned-wrapper/pvd-checkbox'))
            )
            asking_again.click()

            very_short_sleep()
            submit_code = wait.until(
                EC.element_to_be_clickable((
                    By.XPATH, '//*[@id="dom-otp-code-submit-button"]'))
            )
            submit_code.click()

            logger.info("Submitted 2FA code via text.")
            short_sleep()

        elif method == 'app':
            # Wait for user to approve app notification
            logger.info("Awaiting app notification approval.")
            # Implement a polling mechanism or a waiting period
            # For simplicity, wait for a certain time and check if login is successful
            short_sleep(15)  # Wait for 15 seconds

            try:
                trade_button = wait.until(
                    EC.element_to_be_clickable((
                        By.XPATH, '//*[@id="action-bar--container"]/div[2]/div[1]/ul/li[1]/a'))
                )
                trade_button.click()
                short_sleep()
                logger.info("App Notification 2FA approved.")
            except TimeoutException:
                logger.error("App Notification 2FA not approved within the expected time.")
                return {'status': 'error', 'message': 'App Notification 2FA not approved.'}

        else:
            logger.error("Invalid 2FA method specified.")
            return {'status': 'error', 'message': 'Invalid 2FA method specified.'}

        short_sleep()
        # After 2FA, proceed with the trade
        if action == 'buy':
            trade_response = buy_after_login(driver, tickers, trade_share_count)
        elif action == 'sell':
            trade_response = sell_after_login(driver, ticker, trade_share_count)
        else:
            logger.error("Invalid trade action specified.")
            return {'status': 'error', 'message': 'Invalid trade action specified.'}

        # Clean up
        driver.quit()
        shutil.rmtree(temp_dir, ignore_errors=True)
        del two_fa_sessions[session_id]

        return trade_response

    except Exception as e:
        logger.error(f"Error during 2FA completion and trade: {str(e)}")
        driver.quit()
        shutil.rmtree(temp_dir, ignore_errors=True)
        del two_fa_sessions[session_id]
        return {'status': 'error', 'message': 'An error occurred during 2FA completion and trade.', 'error': str(e)}


def buy(tickers, dir, prof, trade_share_count, username, password, two_fa_code=None):
    logger.info(f"Initiating buy operation for {trade_share_count} shares of {tickers} by user {username}")
    driver, temp_dir = start_headless_driver(dir, prof)
    try:
        driver.get("https://digital.fidelity.com/ftgw/digital/portfolio/summary")
        login_response = login(driver, temp_dir, username, password)

        if login_response['status'] == '2FA_required':
            logger.info(f"2FA required via {login_response['method']}.")
            # Store action details in the session
            session_id = login_response.get('session_id')
            two_fa_sessions[session_id]['action'] = 'buy'
            two_fa_sessions[session_id]['tickers'] = tickers
            two_fa_sessions[session_id]['trade_share_count'] = trade_share_count
            return {
                'status': '2FA_required',
                'method': login_response['method'],
                'session_id': session_id,
                'message': '2FA is required. Please provide the 2FA code.'
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
        account_count = getNumOfAccounts(driver)
        very_short_sleep()

        logger.info(f"Number of accounts found: {account_count}")
        print("Iterating through accounts now...")
        for num in range(account_count):
            if num != 0:
                account_dropdown = driver.find_element(By.XPATH, '//*[@id="dest-acct-dropdown"]')
                account_dropdown.click()
            very_short_sleep()
            switchAccounts(driver, num)
            short_sleep()

            for ticker in tickers:
                ticker_search(driver, ticker)

                print("Clicking buy...")
                logger.info(f"Attempting to buy {trade_share_count} shares of {ticker}")
                # Click buy
                buy_button = driver.find_element(By.XPATH, '//*[@id="action-buy"]/s-root/div')
                buy_button.click()
                very_short_sleep()

                print("Entering quantity...")
                logger.info(f"Entering quantity: {trade_share_count}")
                # Enter quantity
                qty_field = driver.find_element(By.XPATH, '//*[@id="eqt-shared-quantity"]')
                human_type(str(trade_share_count), qty_field)
                very_short_sleep()

                # Click somewhere else to trigger events
                price_area = driver.find_element(By.XPATH, '//*[@id="quote-panel"]/div/div[2]')
                price_area.click()
                very_short_sleep()

                # Click limit buy
                limit_buy_button = driver.find_element(By.XPATH, '//*[@id="market-no"]/s-root/div/label')
                limit_buy_button.click()
                very_short_sleep()

                # Get current price and adjust
                current_price = driver.execute_script('return document.querySelector("#eq-ticket__last-price .last-price").textContent')
                current_price = float(current_price[1:])  # Removes '$'
                current_price += 0.1  # Adjust for higher odds in order fill
                current_price = f"{current_price:.2f}"

                # Enter limit price
                limit_price = driver.find_element(By.XPATH, '//*[@id="eqt-ordsel-limit-price-field"]')
                human_type(current_price, limit_price)
                very_short_sleep()

                preview_and_submit(driver)

                # Start a new order
                start_new_order(driver)

        print("No more accounts to process.")
        return {
            'status': 'success',
            'message': f'Bought {trade_share_count} shares of {tickers} through Fidelity.',
            'data': {
                'tickers': tickers,
                'quantity': trade_share_count,
            }
        }

    except Exception as e:
        logger.error(f"Error during buy_after_login operation: {str(e)}")
        return {
            'status': 'failure',
            'message': f'Failed to buy {tickers}.',
            'error': str(e)
        }


def sell(ticker, dir, prof, trade_share_count, username, password, two_fa_code=None):
    logger.info(f"Initiating sell operation for {trade_share_count} shares of {ticker} by user {username}")
    driver, temp_dir = start_headless_driver()
    try:
        driver.get("https://digital.fidelity.com/ftgw/digital/portfolio/summary")
        login_response = login(driver, username, password)

        if login_response['status'] == '2FA_required':
            logger.info(f"2FA required via {login_response['method']}.")
            # Store action details in the session
            session_id = login_response.get('session_id')
            two_fa_sessions[session_id]['action'] = 'sell'
            two_fa_sessions[session_id]['ticker'] = ticker
            two_fa_sessions[session_id]['trade_share_count'] = trade_share_count
            return {
                'status': '2FA_required',
                'method': login_response['method'],
                'session_id': session_id,
                'message': '2FA is required. Please provide the 2FA code.'
            }

        elif login_response['status'] == 'success':
            # Proceed with selling
            trade_response = sell_after_login(driver, ticker, trade_share_count)
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
            'message': f'Failed to sell {ticker}.',
            'error': str(e)
        }

def sell_after_login(driver, ticker, trade_share_count):
    try:
        account_count = getNumOfAccounts(driver)
        very_short_sleep()

        logger.info(f"Number of accounts found: {account_count}")
        print("Iterating through accounts now...")
        for num in range(account_count):
            if num != 0:
                account_dropdown = driver.find_element(By.XPATH, '//*[@id="dest-acct-dropdown"]')
                account_dropdown.click()
            very_short_sleep()
            switchAccounts(driver, num)
            short_sleep()

            ticker_search(driver, ticker)

            # Click sell
            print("Clicking sell...")
            logger.info(f"Attempting to sell {trade_share_count} shares of {ticker}")
            sell_button = driver.find_element(By.XPATH, '//*[@id="action-sell"]/s-root/div')
            sell_button.click()
            very_short_sleep()

            print("Entering quantity...")
            logger.info(f"Entering quantity: {trade_share_count}")
            # Enter quantity
            qty_field = driver.find_element(By.XPATH, '//*[@id="eqt-shared-quantity"]')
            qty_field.click()
            very_short_sleep()
            if str(trade_share_count).lower() == "all":   # sell all
                sell_all_button = driver.find_element(By.XPATH, '//*[@id="stock-quatity"]/div/div[2]/div/pvd3-button')
                sell_all_button.click()
            else:   # sell user specified
                human_type(str(trade_share_count), qty_field)
            very_short_sleep()

            # Click somewhere else to trigger events
            price_area = driver.find_element(By.XPATH, '//*[@id="quote-panel"]/div/div[2]')
            price_area.click()
            very_short_sleep()

            # Click market sell
            market_sell_button = driver.find_element(By.XPATH, '//*[@id="market-yes"]/s-root/div/label')
            market_sell_button.click()
            very_short_sleep()

            preview_and_submit(driver)

            # Start a new order
            start_new_order(driver)

        print("No more accounts to process.")
        return {
            'status': 'success',
            'message': f'Sold {trade_share_count} shares of {ticker} through Fidelity.',
            'data': {
                'ticker': ticker,
                'quantity': trade_share_count,
            }
        }

    except Exception as e:
        logger.error(f"Error during sell_after_login operation: {str(e)}")
        return {
            'status': 'failure',
            'message': f'Failed to sell {ticker}.',
            'error': str(e)
        }
    

def getNumOfAccounts(driver):
    short_sleep()

    # click trade
    try:
        trade_button = WebDriverWait(driver,10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="action-bar--container"]/div[2]/div[1]/ul/li[1]/a'))
        )
        trade_button.click()
        short_sleep()
    except:
        print("Could not find trade button...")

    # click account selection dropdown
    print("clicking dropdown...")

    try:
        account_dropdown = WebDriverWait(driver,10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="dest-acct-dropdown"]'))
        )
        account_dropdown.click()
    except:
        print("dropdown not found")

    try:
        ul_element = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="ett-acct-sel-list"]/ul'))
        )
        li_elements = ul_element.find_elements(By.TAG_NAME, 'li')
        return len(li_elements) 
    except:
        print("Could not get the number of accounts...")

def ticker_search(driver, ticker):
    search = driver.find_element(By.XPATH, '//*[@id="eq-ticket-dest-symbol"]')

    # enter ticker
    human_type(ticker, search)
    very_short_sleep()
    search.send_keys(Keys.ENTER)
    very_short_sleep()

def preview_and_submit(driver):
    print("previewing... ")
    # preview button
    preview_button = driver.find_element(By.XPATH, '//*[@id="previewOrderBtn"]/s-root/button')
    preview_button.click()
    very_short_sleep()

    print("submitting...")
    # submit
    try:
        submit_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="placeOrderBtn"]'))
        )
        submit_button.click()
        print("order successfully submitted!")
    except:
        print("Could not submit order...")
    short_sleep()
    

def start_new_order(driver):
    new_order_button = driver.find_element(By.XPATH, '//*[@id="eq-ticket__enter-new-order"]')
    new_order_button.click()
    short_sleep()

def switchAccounts(driver, num):
    try:
        account_select = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, f'//*[@id="account{num}"]'))    
        )
        account_select.click()
    except:
        print("Could not switch accounts...")