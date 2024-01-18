from flask import Flask, jsonify, render_template_string
import json
import sqlite3
from osrsdb.cleanup import clean_database
from osrsdb.process import process_and_store_api_data
from osrsdb.database import create_connection

app = Flask(__name__)

def fetch_data():
    conn = create_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM items')
    items = cursor.fetchall()
    conn.close()
    return [dict(row) for row in items]

@app.route('/')
def index():
    initial_data = fetch_data()
    return render_template_string(open('static/index.html').read(), initial_data=json.dumps(initial_data))

@app.route('/get-data')
def get_data():
    process_and_store_api_data()
    clean_database()
    return jsonify(fetch_data())

@app.route('/get-history/<int:item_id>')
def get_history(item_id):
    conn = create_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM item_history WHERE item_id = ?', (item_id,))
    history = cursor.fetchall()
    conn.close()
    return jsonify([dict(row) for row in history])

if __name__ == '__main__':
    app.run(debug=True)