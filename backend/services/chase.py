from utils.sleep import *
import time

# ENTER YOUR CREDENTIALS
username = ""   # ENTER YOUR USERNAME
pw = ""         # ENTER YOUR PASSWORD


# TODO:
# add multi buy function
# add 2fa handling
def login(driver):
    wait = WebDriverWait(driver, 30)
    # Sign-in field
    try:
        driver.find_elements(By.TAG_NAME, "iframe")
        # Switch to the iframe using its id
        wait.until(EC.frame_to_be_available_and_switch_to_it((By.ID, "logonbox")))
        very_short_sleep()

        # Get username
        username_field = wait.until(lambda d: d.execute_script(
            'return document.querySelector("#userId").shadowRoot.querySelector("#userId-input")'))
        driver.execute_script('arguments[0].click();', username_field)
        very_short_sleep()

        human_type(username, username_field)

        short_sleep()
        
        # Get password
        pw_field = wait.until(lambda d: d.execute_script(
            'return document.querySelector("#password").shadowRoot.querySelector("#password-input")'))
        driver.execute_script('arguments[0].click();', pw_field)
        human_type(pw, pw_field)

        # Click remember me box
        driver.execute_script(
            "var checkbox = document.querySelector('mds-checkbox#rememberMe'); checkbox.setAttribute('state', 'true'); return checkbox;"
        )

        short_sleep()

        # Click sign in button
        signin = driver.execute_script(
            'return document.querySelector("#signin-button").shadowRoot.querySelector("button")')
        short_sleep()
        driver.execute_script('arguments[0].click();', signin)

    except Exception as e:
        print(f"An error occurred during login: {e}")

    # Sent 2FA as text
    try:
        send_text_btn = wait.until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="header-simplerAuth-dropdownoptions-styledselect"]'))
        )
        send_text_btn.click()

        phone_num = driver.find_element(By.XPATH, '//*[@id="container-1-simplerAuth-dropdownoptions-styledselect"]')
        phone_num.click()

        submit_btn = driver.find_element(By.XPATH, '//*[@id="requestIdentificationCode"]')
        submit_btn.click()

        code = input("\n\nEnter the code sent to your phone: ")
        code_input = driver.find_element(By.XPATH, '//*[@id="otpcode_input-input-field"]')
        human_type(code, code_input)

        pw_input = driver.find_element(By.XPATH, '//*[@id="password_input-input-field"]')
        human_type(pw, pw_input)

        submit_btn = driver.find_element(By.XPATH, '//*[@id="log_on_to_landing_page-sm"]')
        submit_btn.click()
    except Exception as e:
        print("Error sending 2FA as text, continuing:", e)

    # Sent 2FA to app
    try:
        # 2FA handling
        shadow_host_selector = "#optionsList"
        shadow_element_selector = "#mds-list__list-items > li > div > a"
        send_noti_btn = wait_for_shadow_element(driver, shadow_host_selector, shadow_element_selector)
    
        if send_noti_btn:
            driver.execute_script('arguments[0].click();', send_noti_btn)
        else:
            print("The button inside the shadow DOM was not found.")
    except Exception as e:
        print(f"An error occurred during 2FA handling: {e}")

def wait_for_shadow_element(driver, shadow_host_css, shadow_element_selector):
    very_short_sleep()
    try:
        WebDriverWait(driver, 10).until(lambda d: d.execute_script(
            f'''
            let shadowHost = document.querySelector("{shadow_host_css}");
            if (!shadowHost) return false;
            let shadowRoot = shadowHost.shadowRoot;
            if (!shadowRoot) return false;
            let element = shadowRoot.querySelector("{shadow_element_selector}");
            return element !== null;
            '''
        ))
        # If found, return the element
        return driver.execute_script(
            f'''
            return document.querySelector("{shadow_host_css}").shadowRoot.querySelector("{shadow_element_selector}");
            '''
        )
    except TimeoutException:
        return None

def buy(tickers, dir, prof, qty):
    """
    Args:
        tickers (list of str): List of stock ticker symbols to buy.
        dir (str): Path to the ChromeDriver executable.
        prof (str): Path to the Chrome user profile.
    """
    driver = None
    try:
        # Initialize WebDriver
        driver = start_regular_driver(dir, prof)
        driver.get("https://secure.chase.com/web/auth/dashboard#/dashboard/overviewAccounts/overview/index")
        wait = WebDriverWait(driver, 30)
        short_sleep()

        login(driver)

        # Uncomment if you want manual confirmation after 2FA
        # os.system('echo \a')
        # input("\n\nPlease complete 2FA if requested and then press Enter when you reach the dashboard...\n\n\n")
        # print("Logged into Chase!")

        short_sleep()

        # Determine the number of account rows
        num_of_rows = driver.execute_script('''
            let shadow_root = document.querySelector("#account-table-INVESTMENT").shadowRoot;
            let tbody = shadow_root.querySelector("tbody");
            return tbody.querySelectorAll("tr").length;
        ''')

        for i in range(num_of_rows):
            short_sleep()
            if driver.current_url != 'https://secure.chase.com/web/auth/dashboard#/dashboard/overview':
                driver.get('https://secure.chase.com/web/auth/dashboard#/dashboard/overview')

            short_sleep()
            script_info = f'''
                return document.querySelector("#account-table-INVESTMENT").shadowRoot
                    .querySelector("#row-header-row{i}-column0 > div > a > span");
            '''
            
            try:
                account_select = wait.until(lambda d: d.execute_script(script_info))
                driver.execute_script('arguments[0].click();', account_select)
                print(f"Selected account {i+1}")
            except Exception as e:
                print(f"Failed to select account {i+1}: {e}")
                continue

            short_sleep()
            account_url = driver.current_url

            for ticker in tickers:
                # Find and select ticker
                try:
                    ticker_search = wait.until(lambda d: d.execute_script(
                        'return document.querySelector("#quoteSearchLink").shadowRoot.querySelector("a")'))
                    driver.execute_script('arguments[0].click();', ticker_search)
                    short_sleep()

                    ticker_input = wait.until(lambda d: d.execute_script(
                        'return document.querySelector("#typeaheadSearchTextInput").shadowRoot.querySelector("#typeaheadSearchTextInput-input")'))
                    driver.execute_script('arguments[0].click()', ticker_input)
                    short_sleep()

                    human_type(ticker, ticker_input)
                    short_sleep()
                    ticker_input.send_keys(Keys.ENTER)
                    long_sleep()
                    driver.find_element(By.TAG_NAME, "iframe")
                    
                    # Switch to the iframe
                    driver.switch_to.frame("quote-markit-thirdPartyIFrameFlyout")
                except Exception as e:
                    print(f"An error occurred while searching for ticker '{ticker}': {e}")
                    continue

                try:
                    wait_short = WebDriverWait(driver, 4)
                    close_button = wait_short.until(
                        EC.visibility_of_element_located((By.XPATH, "//*[@id='close-add-market-alert-notification']"))
                    )
                    close_button.click()
                    rand_sleep()
                except TimeoutException:
                    print("\n\nNo market alert notification found, continuing with buy...\n\n")

                # Purchase ticker
                try:
                    trade_button = wait.until(
                        EC.visibility_of_element_located((By.XPATH, '//*[@id="quote-header-trade-button"]'))
                    )
                    trade_button.click()

                    rand_sleep()
                    driver.switch_to.default_content()

                    # Buy
                    buy_button = driver.find_element(By.XPATH, '//*[@id="orderAction-segmentedButtonInput-0"]')
                    buy_button.click()

                    short_sleep()

                    # Dropdown order type
                    order_type_dropdown = wait.until(lambda d: d.execute_script(
                        'return document.querySelector("#orderTypeDropdown").shadowRoot.querySelector("#select-orderTypeDropdown")'))
                    driver.execute_script('arguments[0].click();', order_type_dropdown)

                    short_sleep()

                    # Choose market order
                    market_order = wait.until(
                        EC.visibility_of_element_located((By.XPATH, '//*[@id="orderTypeDropdown"]/mds-select-option[1]'))
                    )
                    market_order.click()

                    short_sleep()

                    # Share quantity
                    share_qty = wait.until(lambda d: d.execute_script(
                        'return document.querySelector("#orderQuantity").shadowRoot.querySelector("#orderQuantity-input")'))
                    driver.execute_script('arguments[0].click();', share_qty)
                    short_sleep()
                    share_qty.send_keys(qty)

                    short_sleep()

                    # Click preview
                    preview_button = wait.until(lambda d: d.execute_script(
                        'return document.querySelector("#previewButton").shadowRoot.querySelector("button")'))
                    driver.execute_script('arguments[0].click();', preview_button)

                    short_sleep()

                    # Click place order
                    place_order_button = driver.execute_script(
                        'return document.querySelector("#orderPreviewContent > div.order-preview-section.mds-pt-4 > div > mds-button").shadowRoot.querySelector("button")')
                    driver.execute_script('arguments[0].click();', place_order_button)

                    print(f"Order placed successfully for '{ticker}' on Chase!")
                    short_sleep()

                    # Navigate back to dashboard
                    driver.get(account_url)

                except Exception as e:
                    print(f"An error occurred while placing order for '{ticker}'")
                    driver.get(account_url)
                    continue

        print("No more accounts to process.")
    finally:
        if driver:
            driver.quit()
            print("WebDriver has been closed.")

def sell(tickers, dir, prof, qty):
    """
    Automate the process of selling specified tickers across all accounts.

    Args:
        tickers (list of str): List of stock ticker symbols to sell.
        dir (str): Path to the ChromeDriver executable.
        prof (str): Path to the Chrome user profile.
        qty (str): Quantity of shares to sell for each ticker.
    """
    driver = None
    try:
        # Initialize WebDriver
        driver = start_regular_driver(dir, prof)
        driver.get("https://secure.chase.com/web/auth/dashboard#/dashboard/overviewAccounts/overview/index")
        wait = WebDriverWait(driver, 30)
        short_sleep()

        # Login to Chase
        login(driver)

        # Uncomment if you want manual confirmation after 2FA
        # os.system('echo \a')
        # input("\n\nPlease complete 2FA if requested and then press Enter when you reach the dashboard...\n\n\n")
        # print("Logged into Chase!")

        short_sleep()

        # Determine the number of account rows
        num_of_rows = driver.execute_script('''
            let shadow_root = document.querySelector("#account-table-INVESTMENT").shadowRoot;
            let tbody = shadow_root.querySelector("tbody");
            return tbody.querySelectorAll("tr").length;
        ''')

        for i in range(num_of_rows):
            short_sleep()
            if driver.current_url != 'https://secure.chase.com/web/auth/dashboard#/dashboard/overview':
                driver.get('https://secure.chase.com/web/auth/dashboard#/dashboard/overview')

            short_sleep()
            script_info = f'''
                return document.querySelector("#account-table-INVESTMENT").shadowRoot
                    .querySelector("#row-header-row{i}-column0 > div > a > span");
            '''
            
            try:
                account_select = wait.until(lambda d: d.execute_script(script_info))
                driver.execute_script('arguments[0].click();', account_select)
                print(f"Selected account {i+1}")
            except Exception as e:
                print(f"Failed to select account {i+1}: {e}")
                continue

            short_sleep()
            account_url = driver.current_url
            for ticker in tickers:
                # Find and select ticker
                try:
                    ticker_search = wait.until(lambda d: d.execute_script(
                        'return document.querySelector("#quoteSearchLink").shadowRoot.querySelector("a")'))
                    driver.execute_script('arguments[0].click();', ticker_search)
                    short_sleep()

                    ticker_input = wait.until(lambda d: d.execute_script(
                        'return document.querySelector("#typeaheadSearchTextInput").shadowRoot.querySelector("#typeaheadSearchTextInput-input")'))
                    driver.execute_script('arguments[0].click()', ticker_input)
                    short_sleep()

                    human_type(ticker, ticker_input) 
                    short_sleep()
                    ticker_input.send_keys(Keys.ENTER)
                    long_sleep()
                    driver.find_element(By.TAG_NAME, "iframe")
                    
                    # Switch to the iframe
                    driver.switch_to.frame("quote-markit-thirdPartyIFrameFlyout")
                except Exception as e:
                    print(f"An error occurred while searching for ticker '{ticker}': {e}")
                    continue

                try:
                    wait_short = WebDriverWait(driver, 4)
                    close_button = wait_short.until(
                        EC.visibility_of_element_located((By.XPATH, "//*[@id='close-add-market-alert-notification']"))
                    )
                    close_button.click()
                    rand_sleep()
                except TimeoutException:
                    print("\n\nNo market alert notification found, continuing with sell...\n\n")

                # Sell ticker
                try:
                    trade_button = wait.until(
                        EC.visibility_of_element_located((By.XPATH, '//*[@id="quote-header-trade-button"]'))
                    )
                    trade_button.click()

                    rand_sleep()
                    driver.switch_to.default_content()

                    # Sell
                    sell_button = driver.find_element(By.XPATH, '//*[@id="orderAction-segmentedButtonInput-1"]')  # Assuming '1' is for sell
                    sell_button.click()

                    short_sleep()

                    # Dropdown order type
                    order_type_dropdown = wait.until(lambda d: d.execute_script(
                        'return document.querySelector("#orderTypeDropdown").shadowRoot.querySelector("#select-orderTypeDropdown")'))
                    driver.execute_script('arguments[0].click();', order_type_dropdown)

                    short_sleep()

                    # Choose market order
                    market_order = wait.until(
                        EC.visibility_of_element_located((By.XPATH, '//*[@id="orderTypeDropdown"]/mds-select-option[1]'))
                    )
                    market_order.click()

                    short_sleep()

                    # Share quantity
                    share_qty = wait.until(lambda d: d.execute_script(
                        'return document.querySelector("#orderQuantity").shadowRoot.querySelector("#orderQuantity-input")'))
                    driver.execute_script('arguments[0].click();', share_qty)
                    short_sleep()
                    share_qty.send_keys(qty)

                    short_sleep()

                    # Click preview
                    preview_button = wait.until(lambda d: d.execute_script(
                        'return document.querySelector("#previewButton").shadowRoot.querySelector("button")'))
                    driver.execute_script('arguments[0].click();', preview_button)

                    short_sleep()

                    # Click place order
                    place_order_button = driver.execute_script(
                        'return document.querySelector("#orderPreviewContent > div.order-preview-section.mds-pt-4 > div > mds-button").shadowRoot.querySelector("button")')
                    driver.execute_script('arguments[0].click();', place_order_button)

                    print(f"Order placed successfully for '{ticker}' on Chase!")
                    short_sleep()

                    # Navigate back to dashboard for the next operation
                    driver.get(account_url)
                except Exception as e:
                    print(f"An error occurred while placing order for '{ticker}': {e}")
                    # Optionally, you can add more error handling or logging here
                    driver.get(account_url)
                    continue

        print("No more accounts to process.")
    finally:
        if driver:
            driver.quit()
            print("WebDriver has been closed.")