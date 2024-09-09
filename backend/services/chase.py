from utils.sleep import *
import time

# ENTER YOUR CREDENTIALS
username = ""   # ENTER YOUR USERNAME
pw = ""         # ENTER YOUR PASSWORD

# TODO:
# add multi buy function
def buy(ticker):
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-blink-features=AutomationControlled")   # bypass automation protection
    driver = webdriver.Chrome(options=options, service=Service("chromedriver.exe"))
    driver.get("https://secure.chase.com/web/auth/dashboard#/dashboard/overviewAccounts/overview/index")
    wait = WebDriverWait(driver, 30)
    short_sleep()

    # sign in field
    try:
        driver.find_elements(By.TAG_NAME, "iframe")
        # Switch to the iframe using its id
        wait.until(EC.frame_to_be_available_and_switch_to_it((By.ID, "logonbox")))
        very_short_sleep()

        # get username
        username_field = wait.until(lambda driver: driver.execute_script('return document.querySelector("#userId").shadowRoot.querySelector("#userId-input")'))
        driver.execute_script('arguments[0].click();', username_field)
        very_short_sleep()

        human_type(username, username_field)

        short_sleep()

        pw_field = wait.until(lambda driver: driver.execute_script('return document.querySelector("#password").shadowRoot.querySelector("#password-input")'))
        driver.execute_script('arguments[0].click();', pw_field)
        human_type(pw, pw_field)

        # click remember me box
        driver.execute_script(
            "var checkbox = document.querySelector('mds-checkbox#rememberMe'); checkbox.setAttribute('state', 'true'); return checkbox;"
        )

        short_sleep()

        signin = driver.execute_script('return document.querySelector("#signin-button").shadowRoot.querySelector("button")')
        short_sleep()
        driver.execute_script('arguments[0].click();', signin)

    except Exception as e:
        print(f"An error occurred: {e}")

    os.system('echo \a')
    input("\n\nPlease complete 2FA if requested and then press Enter when you reach the dashboard...\n\n\n")
    print("Logged into Chase!")

    short_sleep()

    num_of_rows = driver.execute_script('''
        let shadow_root = document.querySelector("#account-table-INVESTMENT").shadowRoot;
        let tbody = shadow_root.querySelector("tbody");
        return tbody.querySelectorAll("tr").length;
    ''')
    
    for i in range(num_of_rows):
        # select account
        script_info = f'''
            return document.querySelector("#account-table-INVESTMENT").shadowRoot
                .querySelector("#row-header-row{i}-column0 > div > a > span");
        '''
        
        account_select = wait.until(lambda driver: driver.execute_script(script_info))
        driver.execute_script('arguments[0].click();', account_select)

        short_sleep()

        # find ticker
        try:
            ticker_search = wait.until(lambda driver: driver.execute_script('return document.querySelector("#quoteSearchLink").shadowRoot.querySelector("a")'))
            driver.execute_script('arguments[0].click();', ticker_search)
            short_sleep()

            ticker_search = wait.until(lambda driver: driver.execute_script('return document.querySelector("#typeaheadSearchTextInput").shadowRoot.querySelector("#typeaheadSearchTextInput-input")'))
            driver.execute_script('arguments[0].click()', ticker_search)
            short_sleep()

            for char in ticker:
                ticker_search.send_keys(char)
                time.sleep(0.1) 
            short_sleep()
            ticker_search.send_keys(Keys.ENTER)
            long_sleep()
            driver.find_element(By.TAG_NAME, "iframe")
                
            # Switch to the iframe
            driver.switch_to.frame("quote-markit-thirdPartyIFrameFlyout")
        except Exception as e:
            print(f"An error occurred: {e}")

        try:
            wait = WebDriverWait(driver, 4)
            close_button = wait.until(
                EC.visibility_of_element_located((By.XPATH, "//*[@id='close-add-market-alert-notification']"))
            )

            close_button.click()
            rand_sleep()
        except TimeoutException:
            print("\n\nContinuing with buy...\n\n")

        # purchase ticker
        trade_button = wait.until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="quote-header-trade-button"]')
            ))
        trade_button.click()

        rand_sleep()
        driver.switch_to.default_content()

        # action (buy/sell)
        buy_button = (driver.find_element(By.XPATH, '//*[@id="orderAction-segmentedButtonInput-0"]'))
        buy_button.click()

        short_sleep()

        # dropdown order type
        order_type_dropdown = wait.until(lambda driver: driver.execute_script('return document.querySelector("#orderTypeDropdown").shadowRoot.querySelector("#select-orderTypeDropdown")'))
        driver.execute_script('arguments[0].click();', order_type_dropdown)

        short_sleep()

        # choose market order
        market_order = wait.until(
            EC.visibility_of_element_located(((By.XPATH, '//*[@id="orderTypeDropdown"]/mds-select-option[1]')
            )))
        market_order.click()

        short_sleep()

        # share quantity
        share_qty = wait.until(lambda driver: driver.execute_script('return document.querySelector("#orderQuantity").shadowRoot.querySelector("#orderQuantity-input")'))
        driver.execute_script('arguments[0].click();', share_qty)
        short_sleep()
        share_qty.send_keys("1")

        short_sleep()

        # click preview
        preview_button = wait.until(lambda driver: driver.execute_script('return document.querySelector("#previewButton").shadowRoot.querySelector("button")'))
        driver.execute_script('arguments[0].click();', preview_button)

        short_sleep()

        # click place order
        place_order_button = driver.execute_script('return document.querySelector("#orderPreviewContent > div.order-preview-section.mds-pt-4 > div > mds-button").shadowRoot.querySelector("button")')
        driver.execute_script('arguments[0].click();', place_order_button)

        print("Order placed successfully on Chase!")
        short_sleep()

        driver.get('https://secure.chase.com/web/auth/dashboard#/dashboard/overview')
        rand_sleep()

    print("No more accounts to process.")

    driver.quit()
