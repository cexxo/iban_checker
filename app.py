from flask import Flask, request, jsonify
from zeep import Client

app = Flask(__name__)

# WSDL SOAP
WSDL_URL = 'https://ssl.ibanrechner.de/soap/?wsdl'
import os

USERNAME = os.environ.get('USERNAME')
PASSWORD = os.environ.get('PASSWORD')


client = Client(WSDL_URL)

@app.route('/validate-iban', methods=['POST'])
def validate_iban():
    data = request.get_json()
    iban = data.get('iban')
    if not iban:
        return jsonify({"error": "IBAN missing"}), 400
    try:
        response = client.service.validate_iban(
            iban=iban,
            user=USERNAME,
            password=PASSWORD,
            account_holder=""
        )
        if response.result.strip().lower() != 'failed':
            status = 'Valid' 
        else:
            status = 'Invalid'
        return jsonify({"iban": iban, "status": response.result})
    except Exception as e:
        return jsonify({"iban": iban, "status": "Error", "error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)






