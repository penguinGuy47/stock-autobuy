from flask import Flask, jsonify
from flask_cors import CORS
from controllers.trade_controller import trade_bp

# Initialize the Flask app
app = Flask(__name__)
CORS(app) 

# Register Blueprints
app.register_blueprint(trade_bp, url_prefix='/api/trade')

# optional health check
# @app.route('/health', methods=['GET'])
# def health_check():
#     return jsonify({"status": "up"}), 200

if __name__ == '__main__':
    app.run(debug=True)