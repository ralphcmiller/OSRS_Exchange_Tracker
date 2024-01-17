from flask import Flask, jsonify, render_template_string
import sqlite3
import json
from osrsdb.fetchprices import update_database
from osrsdb.cleanupdb import clean_database

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('osrs_prices.db')
    conn.row_factory = sqlite3.Row
    return conn

def fetch_data():
    conn = get_db_connection()
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
    update_database()
    clean_database()
    return jsonify(fetch_data())

@app.route('/get-history/<int:item_id>')
def get_history(item_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM item_history WHERE item_id = ?', (item_id,))
    history = cursor.fetchall()
    conn.close()
    return jsonify([dict(row) for row in history])

if __name__ == '__main__':
    app.run(debug=True)