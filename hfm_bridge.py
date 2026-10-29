import MetaTrader5 as mt5
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def init_mt5():
    # REPLACE WITH YOUR ACTUAL HFM LOGIN DETAILS
    login_id = 57558283                 # Your HFM MT5 Account Number (Integer)
    password = "_Strathpeter210"    # Your MT5 Trading Password (String)
    server = "HFMarketsKE-Demo2"          # Your exact HFM Server name (e.g., HFMarketsSC-Live or Demo)

    if not mt5.initialize(login=login_id, password=password, server=server):
        print("❌ MT5 Initialization Failed, error code =", mt5.last_error())
        return False
    
    print("✅ Connected to HFM MetaTrader 5 Terminal Successfully!")
    return True

@app.route('/trade-basket', methods=['POST'])
def place_trade():
    data = request.json
    symbol = data.get('symbol')
    order_type = data.get('order_type')
    entry = float(data.get('entry'))
    sl = float(data.get('sl'))
    tp = float(data.get('tp'))
    
    # Map order types to MetaTrader5 constants
    type_mt5 = {
        "BUY_LIMIT": mt5.ORDER_TYPE_BUY_LIMIT,
        "SELL_LIMIT": mt5.ORDER_TYPE_SELL_LIMIT,
        "BUY": mt5.ORDER_TYPE_BUY,
        "SELL": mt5.ORDER_TYPE_SELL
    }.get(order_type)

    request_payload = {
        "action": mt5.TRADE_ACTION_PENDING if "LIMIT" in order_type else mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": 0.01, # Default lot size
        "type": type_mt5,
        "price": entry,
        "sl": sl,
        "tp": tp,
        "deviation": 20,
        "magic": 202610,
        "comment": "VibeTrade AI Order",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_IOC,
    }

    result = mt5.order_send(request_payload)
    if result.retcode != mt5.TRADE_RETCODE_DONE:
        return jsonify({"status": "error", "message": result.comment}), 500

    return jsonify({"status": "success", "order_id": result.order})

if __name__ == '__main__':
    if init_mt5():
        print("🚀 HFM Bridge running on http://localhost:5000")
        app.run(host='0.0.0.0', port=5000)