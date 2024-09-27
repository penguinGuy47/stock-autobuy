from flask import Blueprint, request, jsonify
from services.fidelity import buy, sell, complete_2fa_and_trade
from services.chase import buy as chase_buy, sell as chase_sell
from services.schwab import buy as schwab_buy, sell as schwab_sell
import logging
import os

trade_bp = Blueprint('trade_bp', __name__)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Map brokers to their respective buy and sell functions
BROKER_SERVICES = {
    'chase': {'buy': chase_buy, 'sell': chase_sell},
    'fidelity': {'buy': buy, 'sell': sell},
    # 'schwab': {'buy': schwab_buy, 'sell': schwab_sell},
}

@trade_bp.route('/buy', methods=['POST'])
def buy_stock():
    try:
        data = request.json
        logger.info(f"Received buy request: {data}")
        tickers = data.get('tickers')
        broker = data.get('broker')
        quantity = data.get('quantity')
        username = data.get('username')
        password = data.get('password')

        # Validate input
        if not all([tickers, broker, quantity, username, password]):
            logger.warning("Missing required fields in buy request.")
            return jsonify({'error': "Missing required fields: tickers, broker, quantity, username, password."}), 400

        broker = broker.lower()
        if broker not in BROKER_SERVICES:
            logger.warning(f"Unsupported broker: {broker}")
            return jsonify({'error': f"Unsupported broker: {broker}"}), 400

        service = BROKER_SERVICES[broker]['buy']
        response = service(
            tickers=tickers,
            dir=None,   # Adjust if you have directory profiles
            prof=None,  # Adjust if you have profiles
            trade_share_count=quantity,
            username=username,
            password=password
        )

        return jsonify(response), 200

    except Exception as e:
        logger.error(f"Error processing buy request: {str(e)}")
        return jsonify({'error': 'An error occurred while processing the buy request.'}), 500

@trade_bp.route('/sell', methods=['POST'])
def sell_stock():
    try:
        data = request.json
        logger.info(f"Received sell request: {data}")
        tickers = data.get('tickers')  # Single ticker
        broker = data.get('broker')
        quantity = data.get('quantity')
        username = data.get('username')
        password = data.get('password')

        # Validate input
        if not all([tickers, broker, quantity, username, password]):
            logger.warning("Missing required fields in sell request.")
            return jsonify({'error': "Missing required fields: ticker, broker, quantity, username, password."}), 400

        broker = broker.lower()
        if broker not in BROKER_SERVICES:
            logger.warning(f"Unsupported broker: {broker}")
            return jsonify({'error': f"Unsupported broker: {broker}"}), 400

        service = BROKER_SERVICES[broker]['sell']
        response = service(
            tickers=tickers,
            dir=None,
            prof=None,
            trade_share_count=quantity,
            username=username,
            password=password
        )

        return jsonify(response), 200

    except Exception as e:
        logger.error(f"Error processing sell request: {str(e)}")
        return jsonify({'error': 'An error occurred while processing the sell request.'}), 500

@trade_bp.route('/complete_2fa', methods=['POST'])
def complete_2fa_endpoint():
    try:
        data = request.json
        logger.info(f"Received 2FA completion request: {data}")
        session_id = data.get('session_id')
        two_fa_code = data.get('two_fa_code')  # Required for text-based 2FA

        if not session_id:
            logger.warning("Missing session_id in 2FA completion request.")
            return jsonify({'error': "Missing session_id."}), 400

        # Validate session_id exists
        from services.fidelity import two_fa_sessions, complete_2fa_and_trade
        from services.chase import two_fa_sessions as chase_two_fa_sessions, complete_2fa_and_trade as chase_complete_2fa_and_trade

        # if session_id not in two_fa_sessions:
        #     logger.warning(f"Invalid session_id: {session_id}")
        #     return jsonify({'error': 'Invalid session_id.'}), 400
        # el
        if session_id in chase_two_fa_sessions:
            trade_response = chase_complete_2fa_and_trade(
                session_id=session_id,
                two_fa_code=two_fa_code
            )
        else:
            logger.warning(f"Invalid session_id: {session_id}")
            return jsonify({'error': 'Invalid session_id.'}), 400

        return jsonify(trade_response), 200

    except Exception as e:
        logger.error(f"Error processing 2FA completion request: {str(e)}")
        return jsonify({'error': 'An error occurred while completing 2FA.'}), 500
