from services.chase import buy as chase_buy, sell as chase_sell
from services.fidelity import buy as fidelity_buy, sell as fidelity_sell
from services.firstrade import buy as firstrade_buy, sell as firstrade_sell
from services.public import buy as public_buy, sell as public_sell
from services.robinhood import buy as robinhood_buy, sell as robinhood_sell
from services.schwab import buy as schwab_buy, sell as schwab_sell
from services.tradier import buy as tradier_buy
from services.tornado import *
from services.sofi import *
from services.webull import *
from services.wellsfargo import *

def main():
    # ticker = input("Enter the ticker you would to purchase: ")
    buy_input = input("Enter stock tickers to BUY, separated by commas (e.g., AAPL,GOOGL,MSFT): ")
    BUY_TICKERS = [ticker.strip().upper() for ticker in buy_input.split(",") if ticker.strip()]
    
    if not BUY_TICKERS:
        print("No valid BUY tickers provided")
    else:
        while True:
            buy_share_count = input("How many shares would you like to buy? Enter an amount: ")
            
            if re.fullmatch(r'\d+', buy_share_count):
                break
            else:
                print("Invalid input. Please enter a valid number.")
    
    sell_input = input("Enter stock tickers to SELL, separated by commas (e.g., AAPL,GOOGL,MSFT): ")
    SELL_TICKERS = [ticker.strip().upper() for ticker in sell_input.split(",") if ticker.strip()]
    
    if not SELL_TICKERS:
        print("No valid SELL tickers provided.")
    else:
        while True:
            sell_share_count = input("How many shares would you like to sell? For all shares, type 'all', else enter an amount: ")
            
            if sell_share_count.lower() == "all":
                break
            elif re.fullmatch(r'\d+', sell_share_count):
                break
            else:
                print("Invalid input. Please enter 'all' or a number.")

    chrome_path = r"C:\Users\kaile\AppData\Local\Google\Chrome\User Data" # add the path to your chrome
    chrome_profile = r"Profile 5" # chawddnge this accordingly


    fidelity_buy(BUY_TICKERS, chrome_path, chrome_profile, buy_share_count)



if __name__ == "__main__":
    main()
