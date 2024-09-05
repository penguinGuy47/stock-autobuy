from sleep import *

# ENTER YOUR CREDENTIALS
username = ""   # ENTER YOUR EMAIL
pw = ""         # ENTER YOUR PASSWORD

# TODO:
# address cookie saving/loading
# add buy
# add account switching
# add multi buy function
def buy(ticker, dir, prof, qty):
    driver = start_regular_driver(dir, prof)
    # driver = start_headless_driver(dir, prof)
    driver.get("https://robinhood.com/us/en/")
    short_sleep()
    try:
        load_cookies(driver, "rh_cookies.pkl")
        driver.refresh()
    except Exception as e:
        print(e)
        print("No cookies available")
        short_sleep()
        driver.get("https://robinhood.com/login")
    short_sleep()
    login(driver)
    setup_trade(driver, ticker)
    enter_share_qty(driver, qty)
    submit_order(driver)
    get_num_accounts()


def sell(ticker, dir, prof, qty):
    driver = start_headless_driver(dir, prof)
    driver.get("https://robinhood.com/login/")
    short_sleep()
    login(driver)
    setup_trade(driver, ticker)

    # navigate to sell
    enter_sell = driver.find_element(By.XPATH, '//*[@id="sdp-ticker-symbol-highlight"]/div[1]/form/div[1]/div/div[1]/div/div/div[2]/div/div/div/div')
    enter_sell.click()

    very_short_sleep()
    enter_share_qty(driver, qty)
    submit_order(driver)


def login(driver):
    wait = WebDriverWait(driver, 7)
    # check if logged in 
    if driver.current_url != "https://robinhood.com/":
        username_field = driver.find_element(By.XPATH, '//*[@id="react_root"]/div[1]/div[2]/div/div/div/div[2]/div/form/div/div[1]/label/div[2]/input')
        username_field.click()
        human_type(username, username_field)
        very_short_sleep()

        pw_field = driver.find_element(By.XPATH, '//*[@id="current-password"]')
        pw_field.click()
        human_type(pw, pw_field)
        very_short_sleep()

        keep_login = driver.find_element(By.XPATH, '//*[@id="react_root"]/div[1]/div[2]/div/div/div/div[2]/div/form/div/div[3]/label/div/div/div')
        keep_login.click()
        very_short_sleep()

        login_button = driver.find_element(By.XPATH, '//*[@id="submitbutton"]/div/button')
        login_button.click()

        os.system('echo \a')
        # App Noti 2FA
        try: 
            # waits up to 30 seconds for user to accept notification
            WebDriverWait(driver, 30).until(
                EC.url_to_be("https://robinhood.com/")
            )
        except TimeoutException:
            print("\n\nError: you did not accept the 2FA request \n\n")

            # SMS 2FA
            try:
                code_input = wait.until(
                    EC.visibility_of_element_located((By.XPATH, '//*[@id="react_root"]/div[3]/div/div[3]/div/div/section/div/div/div/div/div[2]/div[2]/div/form/div/div/input'))
                )
                driver.save_screenshot("headless_login_page.png")
                sent_code = input("Please enter the 2FA code sent to your phone: ")
                human_type(sent_code, code_input)
                very_short_sleep()

                continue_button = driver.find_element(By.XPATH, '//*[@id="react_root"]/div[3]/div/div[3]/div/div/section/div/div/div/div/div[2]/div[3]/div[1]/div/button')
                continue_button.click()
                short_sleep()
                driver.get("https://robinhood.com/us/en/")
                short_sleep()
                save_cookies(driver, "rh_cookies.pkl")
            except TimeoutException:
                print("SMS 2FA input timed out.")
                # restart_driver()
            
        driver.save_screenshot("headless_login_page.png")
        print("\n\nSuccessfully logged into Robinhood\n\n")
        short_sleep()


def setup_trade(driver, ticker):
    # searches the ticker
    ticker_search = driver.find_element(By.XPATH, '//*[@id="downshift-42-input"]')
    ticker_search.click()
    human_type(ticker, ticker_search)
    very_short_sleep()
    ticker_search.send_keys(Keys.ARROW_DOWN)
    ticker_search.send_keys(Keys.ENTER)
    very_short_sleep()

def enter_share_qty(driver, qty):
    # enter number of shares shares
    shares_dropdown = driver.find_element(By.XPATH, '//*[@id="downshift-120-toggle-button"]')
    shares_dropdown.click();
    very_short_sleep()

    shares_button = driver.find_element(By.XPATH, '//*[@id="af1eca935-ccf1-40f2-87c9-f9a7645b6d15-options-menu-list-option-share"]')
    shares_button.click()
    very_short_sleep()

    shares_qty = driver.find_element(By.XPATH, '//*[@id="sdp-ticker-symbol-highlight"]/div[1]/form/div[2]/div/div[3]/div/div/div/div/input')
    human_type(qty, shares_qty)
    very_short_sleep()


def submit_order(driver):
    submit_button = driver.find_element(By.XPATH, '//*[@id="sdp-ticker-symbol-highlight"]/div[1]/form/div[3]/div/div[2]/div/div/button')
    submit_button.click()
    very_short_sleep()
    verify_submit = driver.find_element(By.XPATH, '//*[@id="sdp-ticker-symbol-highlight"]/div[1]/form/div[3]/div/div[2]/div[1]/div/button')
    verify_submit.click()
    very_short_sleep()
    done_button = driver.find_element(By.XPATH, '//*[@id="sdp-ticker-symbol-highlight"]/div[1]/div/div[3]/div[1]/button')
    done_button.click()
    short_sleep()

def get_num_accounts(driver):
    initial_dropdown = driver.find_element(By.XPATH, '//*[@id="sdp-ticker-symbol-highlight"]/div[1]/form/button')
    initial_dropdown.click()
    very_short_sleep()

    div = driver.find_element(By.XPATH, '//*[@id="account-switcher-popover"]/div')
    accounts = div.find_elements(By.TAG_NAME, 'button')
    num_accounts = len(accounts)
    # //*[@id="account-switcher-popover"]/div/button[1]
    # //*[@id="account-switcher-popover"]/div/button[2]

    return num_accounts 

def switch_accounts(driver, account_num):
    pass
    


