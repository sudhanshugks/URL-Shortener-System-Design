import sqlite3
import string
import random
from flask import Flask, request, redirect, jsonify, abort

app = Flask(__name__)
DB_FILE = 'urls.db'

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS url_map (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            short_code TEXT UNIQUE NOT NULL,
            long_url TEXT NOT NULL
        )
    ''')
    # Add index for faster lookups during redirection
    c.execute('CREATE INDEX IF NOT EXISTS idx_short_code ON url_map(short_code)')
    conn.commit()
    conn.close()

def generate_short_code(length=6):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))

@app.route('/shorten', methods=['POST'])
def shorten_url():
    data = request.get_json()
    if not data or 'url' not in data:
        return jsonify({'error': 'Missing URL parameter'}), 400
    
    long_url = data['url']
    short_code = generate_short_code()
    
    try:
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        c.execute('INSERT INTO url_map (short_code, long_url) VALUES (?, ?)', (short_code, long_url))
        conn.commit()
    except sqlite3.Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if conn:
            conn.close()
            
    return jsonify({
        'short_url': f"http://localhost:5000/{short_code}",
        'short_code': short_code,
        'long_url': long_url
    }), 201

@app.route('/<short_code>', methods=['GET'])
def redirect_url(short_code):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('SELECT long_url FROM url_map WHERE short_code = ?', (short_code,))
    result = c.fetchone()
    conn.close()
    
    if result:
        return redirect(result[0], code=302)
    else:
        abort(404)

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, threaded=True)
