from utils.sleep import *

# ENTER YOUR CREDENTIALS
username = ""   # ENTER YOUR USERNAME
pw = ""         # ENTER YOUR PASSWORD

# TODO:
# add multi buy function
def buy(ticker, dir, prof):
    while True:
        trade_share_count = input("How many shares would you like to buy? Enter an amount: ")
        
        if re.fullmatch(r'\d+', trade_share_count):
            break
        else:
            print("Invalid input. Please enter a valid number.")
            
    driver = start_headless_driver(dir, prof)
    driver.get("https://invest.firstrade.com/cgi-bin/login")
    login(driver)
    short_sleep()
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
        setup_trade(driver, account, bought_accounts, ticker)

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


def sell(ticker, dir, prof):
    while True:
        trade_share_count = input("How many shares would you like to buy? Enter an amount: ")
        
        if re.fullmatch(r'\d+', trade_share_count):
            break
        else:
            print("Invalid input. Please enter a valid number.")


# login and 2FA handling
def login(driver):
    username_field = driver.find_element(By.XPATH, '//*[@id="username"]')
    username_field.click()
    human_type(username, username_field)

    pw_field = driver.find_element(By.XPATH, '//*[@id="password"]')
    human_type(pw, pw_field)
    short_sleep()

    submit_button = driver.find_element(By.XPATH, '//*[@id="loginButton"]')
    submit_button.click()

    try:
        send_by_text = WebDriverWait(driver, 24).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="form-recipients"]/label[2]/div/div[1]/input'))
        )
        send_by_text.click()
        send_code = WebDriverWait(driver, 24).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="send-code"]'))
        )
        send_code.click()

        verify_code = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="code"]'))
        )

        code = input("Please enter the 2FA code sent to your phone: ")
        human_type(code, verify_code)

        submit_code = driver.find_element(By.XPATH, '//*[@id="verify-code"]')
        submit_code.click()
        print("Logged into First Trade!")
    except:
        print("2FA authentication failed.")

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
def setup_trade(driver, account, bought_accounts, ticker):
    if account != 1:
            try:
                account_dropdown = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '//*[@id="head"]/ul/li[7]/div'))
                )
                account_dropdown.click()
                short_sleep()
            except:
                print("\n\nError in clicking dropdown...\n\n")
    try:
        current_account = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, f'//*[@id="headcontent"]/div[3]/div[2]/table/tbody/tr[{account}]/th/a'))
        )
        bought_accounts.add(current_account.text)
        current_account.click()
        short_sleep()

        # input ticker
        ticker_search = driver.find_element(By.XPATH, '//*[@id="id-symlookup"]')
        ticker_search.clear()
        very_short_sleep()
        human_type(ticker, ticker_search)
        very_short_sleep()

        # click on search
        ticker_search = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="id-searchbtngo"]'))
        )
        ticker_search.click()
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