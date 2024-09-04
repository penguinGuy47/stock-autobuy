from sleep import *

# ENTER YOUR CREDENTIALS
username = ""   # ENTER YOUR EMAIL
pw = ""         # ENTER YOUR PASSWORD

# TODO:
# address cookie saving/loading
# add buy
# add account switching
# add multi buy function
def buy(ticker, dir, prof):
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

def sell(ticker, dir, prof):
    driver = start_headless_driver(dir, prof)
    driver.get("https://robinhood.com/login/")
    short_sleep()
    login(driver)

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

        try:
            code_input = wait.until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="react_root"]/div[3]/div/div[3]/div/div/section/div/div/div/div/div[2]/div[2]/div/form/div/div/input'))
            )
            driver.save_screenshot("headless_login_page.png")
            os.system('echo \a')
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
            pass
        driver.save_screenshot("headless_login_page.png")
        print("\n\nSuccessfully logged into Robinhood\n\n")
        time.sleep(10000)

