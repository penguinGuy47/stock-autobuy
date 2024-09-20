from flask import Blueprint, request, jsonify
from services.chase import buy as chase_buy, sell as chase_sell
from services.fidelity import buy as fidelity_buy, sell as fidelity_sell
from services.firstrade import buy as firstrade_buy, sell as firstrade_sell
from services.public import buy as public_buy, sell as public_sell
from services.robinhood import buy as robinhood_buy, sell as robinhood_sell
from services.schwab import buy as schwab_buy, sell as schwab_sell
from services.tradier import buy as tradier_buy, sell as tradier_sell
import logging

trade_bp = Blueprint('trade_bp', __name__)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# map brokers to their respective buy and sell functions
BROKER_SERVICES = {
    'chase': {'buy': chase_buy, 'sell': chase_sell},
    'fidelity': {'buy': fidelity_buy, 'sell': fidelity_sell},
    'schwab': {'buy': schwab_buy, 'sell': schwab_sell},
}

def handle_trade(action):
    try:
        data = request.json
        ticker = data.get('ticker')
        broker = data.get('broker')
        quantity = data.get('quantity')
        username = data.get('username')
        password = data.get('password')

        # Validate input
        if not all([ticker, broker, quantity, username, password]):
            logger.warning("Missing required fields in request data.")
            return jsonify({'error': "Missing required fields: ticker, broker, quantity, username, password."}), 400

        broker = broker.lower()
        if broker not in BROKER_SERVICES:
            logger.warning(f"Unsupported broker: {broker}")
            return jsonify({'error': f"Unsupported broker: {broker}"}), 400

        service = BROKER_SERVICES[broker][action]
        response = service(ticker, quantity, username, password)
        return jsonify(response), 200

    except Exception as e:
        logger.error(f"Error during {action} operation: {str(e)}")
        return jsonify({'error': f"An error occurred during {action} operation."}), 500

@trade_bp.route('/buy', methods=['POST'])
def buy_stock():
    return handle_trade('buy')

@trade_bp.route('/sell', methods=['POST'])
def sell_stock():
    return handle_trade('sell')
