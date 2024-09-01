from sleep import *

# ENTER YOUR CREDENTIALS
username = ""   # ENTER YOUR USERNAME
pw = ""         # ENTER YOUR PASSWORD

# TODO:
# add multi buy function
def buy(ticker, dir, prof):
    options = webdriver.ChromeOptions()
    options.add_argument(f"user-data-dir={dir}")
    options.add_argument(f"--profile-directory={prof}")
    options.add_argument("--disable-blink-features=AutomationControlled")   # bypass automation protection
    driver = webdriver.Chrome(options=options, service=Service("chromedriver.exe"))
    # driver.get("https://digital.fidelity.com/prgw/digital/login/full-page")
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

        # click buy
        buy_button = driver.find_element(By.XPATH, '//*[@id="action-buy"]/s-root/div')
        buy_button.click()
        very_short_sleep()

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

        # preview button
        preview_button = driver.find_element(By.XPATH, '//*[@id="previewOrderBtn"]/s-root/button')
        preview_button.click()
        very_short_sleep()

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

def sell(ticker, dir, prof):
    while True:
        sell_share_count = input("How many shares would you like to sell? For all shares, type 'all', else enter an amount: ")
        
        if sell_share_count.lower() == "all":
            break
        elif re.fullmatch(r'\d+', sell_share_count):
            break
        else:
            print("Invalid input. Please enter 'all' or a number.")
        

    options = webdriver.ChromeOptions()
    options.add_argument(f"user-data-dir={dir}")
    options.add_argument(f"--profile-directory={prof}")
    options.add_argument("--disable-blink-features=AutomationControlled")   # bypass automation protection
    driver = webdriver.Chrome(options=options, service=Service("chromedriver.exe"))
    # driver.get("https://digital.fidelity.com/prgw/digital/login/full-page")
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
    