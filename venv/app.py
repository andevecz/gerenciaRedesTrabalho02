from flask import Flask, request, jsonify
import hashlib
import requests

app = Flask(__name__)

HIBP_API_URL = "https://api.pwnedpasswords.com/range/"

@app.route('/check_password', methods=['POST'])
def check_password():
    data = request.json
    password = data.get("password", "")
    
    if not password:
        return jsonify({"error": "Senha não fornecida"}), 400

    sha1_hash = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    prefix = sha1_hash[:5]
    suffix = sha1_hash[5:]

    try:
        response = requests.get(HIBP_API_URL + prefix)
        response.raise_for_status()

        hashes = response.text.splitlines()
        breaches = 0
        for line in hashes:
            h, count = line.split(':')
            if h == suffix:
                breaches = int(count)
                break

        return jsonify({"breaches": breaches})

    except requests.RequestException as e:
        return jsonify({"error": "Erro ao acessar a API do HIBP", "details": str(e)}), 500

if __name__ == '__main__':
    app.run(port=5000)
