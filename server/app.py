from flask import Flask, request, jsonify
from database import init_db, log_to_db, sqlite3

app = Flask(__name__)

@app.route('/alert', methods=['POST'])
def alert():
    data = request.json
    log_to_db(data['ip'], data['port'], data['service'], data['payload'])
    return jsonify({"status": "logged"}), 200

@app.route('/events', methods=['GET'])
def get_events():
    conn = sqlite3.connect('mirage_events.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM events ORDER BY timestamp DESC LIMIT 50')
    rows = cursor.fetchall()
    conn.close()
    return jsonify([dict(ix) for ix in rows])

if __name__ == '__main__':
    init_db()
    app.run(port=5000, debug=True)