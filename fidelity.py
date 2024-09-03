from sleep import *

# ENTER YOUR CREDENTIALS
username = ""
pw = ""

# TODO:
# add multi buy function
def buy(ticker, dir, prof):
    driver = start_headless_driver(dir, prof)
    driver.get("https://digital.fidelity.com/ftgw/digital/portfolio/summary")
    wait = WebDriverWait(driver, 7)
    short_sleep()

    username_field = driver.find_element(By.XPATH, '//*[@id="dom-username-input"]')
    username_field.click()
    human_type(username, username_field)

    short_sleep()

    pw_field = driver.find_element(By.XPATH, '//*[@id="dom-pswd-input"]')
    human_type(pw, pw_field)
    short_sleep()

    print("clicking login...")
    log_in_button = driver.find_element(By.XPATH, '//*[@id="dom-login-button"]')
    log_in_button.click()

    # TESTING
    short_sleep()
    driver.save_screenshot("headless_login_page.png")
    rand_sleep()

    # IF 2FA PAGE, PING USER (AND SAVE COOKIES?), ELSE WAIT AND CONTINUE
    try:
        dont_ask_again_button = wait.until(
            EC.presence_of_element_located((By.XPATH, "//*[@id='dom-widget']/div/div[2]/pvd-field-group/s-root/div/div/s-slot/s-assigned-wrapper/pvd-form/s-root/div/form/s-slot/s-assigned-wrapper/div[1]/div/div/pvd-field-group/s-root/div/div/s-slot/s-assigned-wrapper/pvd-checkbox/s-root/div/label/div[1]')"))
        )
        dont_ask_again_button.click()

        # send_2fa_button = wait.until(
        #     EC.visibility_of_element_located(By.XPATH, '//*[@id="dom-push-primary-button"]')
            
        # )
        # send_2fa_button.click()

        send_as_text = wait.until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="dom-try-another-way-link"]'))
        )
        send_as_text.click()

        text_code_button = wait.until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="dom-channel-list-primary-button"]'))
        )
        text_code_button.click()
        very_short_sleep()

        os.system('echo \a')
        sent_code = input("Please enter the 2FA code sent to your phone: ")
        code_input = wait.until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="dom-otp-code-input"]'))
        )
        human_type(sent_code, code_input)

        asking_again = wait.until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="dom-widget"]/div/div[2]/pvd-field-group/s-root/div/div/s-slot/s-assigned-wrapper/pvd-form/s-root/div/form/s-slot/s-assigned-wrapper/div[1]/pvd-field-group/s-root/div/div/s-slot/s-assigned-wrapper/pvd-checkbox/s-root/div/label/div[1]'))
        )
        asking_again.click()

        very_short_sleep()
        submit_code = wait.until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="dom-otp-code-submit-button"]'))
        )
        submit_code.click()
    except:
        print("Cookies are saved, continuing...")

    # os.system('echo \a')
    # input("\n\nPlease complete 2FA if requested and then press Enter when you reach the dashboard...\n\n\n")
    # print("Logged into Fidelity!")

    save_cookies(driver, "cookies.pkl")
    short_sleep()

    # driver = start_headless_driver(dir, prof)
    # driver.get("https://digital.fidelity.com/ftgw/digital/portfolio/summary")
    # print("starting headless session...")
    
    # load_cookies(driver, "cookies.pkl")
    # driver.get("https://digital.fidelity.com/ftgw/digital/portfolio/summary")
    # short_sleep()
    # driver.save_screenshot("headless_trade_page.png")

    # click trade
    trade_button = driver.find_element(By.XPATH, '//*[@id="action-bar--container"]/div[2]/div[1]/ul/li[1]/a')
    trade_button.click()
    short_sleep()

    print("clicking dropdown...")
    # click dropdown
    try:
        account_dropdown = wait.until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="dest-acct-dropdown"]'))
        )
        account_dropdown.click()
    except:
        print("dropdown not found")
    very_short_sleep()

    account_select = driver.find_element(By.XPATH, '//*[@id="ett-acct-sel-list"]')
    very_short_sleep()

    ul_element = driver.find_element(By.XPATH, '//*[@id="ett-acct-sel-list"]/ul')
    li_elements = ul_element.find_elements(By.TAG_NAME, 'li')
    li_count = len(li_elements)

    # iterate through accounts
    for num in range(li_count):
        print("iterating through accounts now...")
        if num != 0:
            account_dropdown = driver.find_element(By.XPATH, '//*[@id="dest-acct-dropdown"]')
            account_dropdown.click()
        very_short_sleep()
        account_select = driver.find_element(By.XPATH, f'//*[@id="account{num}"]')
        account_select.click()
        short_sleep()

        ticker_search = driver.find_element(By.XPATH, '//*[@id="eq-ticket-dest-symbol"]')

        # enter ticker
        human_type(ticker, ticker_search)
        very_short_sleep()
        ticker_search.send_keys(Keys.ENTER)
        very_short_sleep()

        print("clicking buy...")
        # click buy
        buy_button = driver.find_element(By.XPATH, '//*[@id="action-buy"]/s-root/div')
        buy_button.click()
        very_short_sleep()

        print("entering qty...")
        # enter quantity
        qty = driver.find_element(By.XPATH, '//*[@id="eqt-shared-quantity"]')
        qty.send_keys("1")
        very_short_sleep()

        # click somewhere else
        price_area = driver.find_element(By.XPATH, '//*[@id="quote-panel"]/div/div[2]')
        price_area.click()
        very_short_sleep()

        # click limit buy
        limit_buy_button = driver.find_element(By.XPATH, '//*[@id="market-no"]/s-root/div/label')
        limit_buy_button.click()
        very_short_sleep()

        # get current price
        current_price = driver.execute_script('return document.querySelector("#eq-ticket__last-price .last-price").textContent')
        current_price = float(current_price[1:]) # removes '$' in front
        current_price += 0.1
        current_price = f"{current_price:.2f}"

        # enter limit price
        limit_price = driver.find_element(By.XPATH, '//*[@id="eqt-ordsel-limit-price-field"]')
        human_type(current_price, limit_price)
        very_short_sleep()

        print("previewing... ")
        # preview button
        preview_button = driver.find_element(By.XPATH, '//*[@id="previewOrderBtn"]/s-root/button')
        preview_button.click()
        very_short_sleep()

        print("submitting...")
        # submit
        submit_button = driver.find_element(By.XPATH, '//*[@id="placeOrderBtn"]')
        submit_button.click()
        short_sleep()

        # enter new order
        new_order_button = driver.find_element(By.XPATH, '//*[@id="eq-ticket__enter-new-order"]')
        new_order_button.click()
        short_sleep()
        
    print("No more accounts to process.")
    driver.quit()

def sell(ticker, dir, prof):
    while True:
        sell_share_count = input("How many shares would you like to sell? For all shares, type 'all', else enter an amount: ")
        
        if sell_share_count.lower() == "all":
            break
        elif re.fullmatch(r'\d+', sell_share_count):
            break
        else:
            print("Invalid input. Please enter 'all' or a number.")
        

    driver = start_headless_driver(dir, prof)
    driver.get("https://digital.fidelity.com/ftgw/digital/portfolio/summary")
    wait = WebDriverWait(driver, 10)
    short_sleep() 

    username_field = driver.find_element(By.XPATH, '//*[@id="dom-username-input"]')
    username_field.click()
    human_type(username, username_field)

    short_sleep()

    pw_field = driver.find_element(By.XPATH, '//*[@id="dom-pswd-input"]')
    human_type(pw, pw_field)
    short_sleep()

    log_in_button = driver.find_element(By.XPATH, '//*[@id="dom-login-button"]')
    log_in_button.click()

    os.system('echo \a')
    input("\n\nPlease complete 2FA if requested and then press Enter when you reach the dashboard...\n\n\n")
    print("Logged into Fidelity!")

    # click trade
    trade_button = driver.find_element(By.XPATH, '//*[@id="action-bar--container"]/div[2]/div[1]/ul/li[1]/a')
    trade_button.click()
    short_sleep()

    # click dropdown
    account_dropdown = driver.find_element(By.XPATH, '//*[@id="dest-acct-dropdown"]')
    account_dropdown.click()
    very_short_sleep()

    account_select = driver.find_element(By.XPATH, '//*[@id="ett-acct-sel-list"]')
    very_short_sleep()

    ul_element = driver.find_element(By.XPATH, '//*[@id="ett-acct-sel-list"]/ul')
    li_elements = ul_element.find_elements(By.TAG_NAME, 'li')
    li_count = len(li_elements)

    # iterate through accounts
    for num in range(li_count):
        if num != 0:
            account_dropdown = driver.find_element(By.XPATH, '//*[@id="dest-acct-dropdown"]')
            account_dropdown.click()
        very_short_sleep()
        account_select = driver.find_element(By.XPATH, f'//*[@id="account{num}"]')
        account_select.click()
        short_sleep()

        ticker_search = driver.find_element(By.XPATH, '//*[@id="eq-ticket-dest-symbol"]')

        # enter ticker
        human_type(ticker, ticker_search)
        very_short_sleep()
        ticker_search.send_keys(Keys.ENTER)
        very_short_sleep()

        # click sell
        sell_button = driver.find_element(By.XPATH, '//*[@id="action-sell"]/s-root/div')
        sell_button.click()
        very_short_sleep()

        # enter quantity
        qty = driver.find_element(By.XPATH, '//*[@id="eqt-shared-quantity"]')
        qty.click()
        very_short_sleep()
        if (sell_share_count == "all"):   # sell all
            sell_all_button = driver.find_element(By.XPATH, '//*[@id="stock-quatity"]/div/div[2]/div/pvd3-button')
            sell_all_button.click()
        else:   # sell user specified
            human_type(sell_share_count, qty)
        very_short_sleep()

        # click somewhere else
        price_area = driver.find_element(By.XPATH, '//*[@id="quote-panel"]/div/div[2]')
        price_area.click()
        very_short_sleep()

        # click market sell
        market_sell_button = driver.find_element(By.XPATH, '//*[@id="market-yes"]/s-root/div/label')
        market_sell_button.click()
        very_short_sleep()

        # get current price for limit order
        # current_price = driver.execute_script('return document.querySelector("#eq-ticket__last-price .last-price").textContent')
        # current_price = float(current_price[1:]) # removes '$' in front
        # current_price += 0.1
        # current_price = f"{current_price:.2f}"
        # enter limit price
        # limit_price = driver.find_element(By.XPATH, '//*[@id="eqt-ordsel-limit-price-field"]')
        # human_type(current_price, limit_price)
        # very_short_sleep()

        # preview button
        preview_button = driver.find_element(By.XPATH, '//*[@id="previewOrderBtn"]/s-root/button')
        preview_button.click()
        very_short_sleep()
        time.sleep(10000)

        # submit
        submit_button = driver.find_element(By.XPATH, '//*[@id="placeOrderBtn"]')
        submit_button.click()
        very_short_sleep()

        # enter new order
        new_order_button = driver.find_element(By.XPATH, '//*[@id="eq-ticket__enter-new-order"]')
        new_order_button.click()
        short_sleep()
        
    print("No more accounts to process.")
    driver.quit()
    