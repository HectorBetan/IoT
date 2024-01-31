from flask import Flask, jsonify
import requests

app = Flask(__name__)

@app.route('/get_data', methods=['GET'])
def get_data():
    try:
        # Headers con el token
        headers = {
            "Authorization": "Token 3thr4pjb6bgvi2zu34yw325kthr30eyrf59k0vs5v9z3m646z4"
            # Reemplaza "YOURAPPTOKENHERE" con tu token real
        }

        # Hacer la solicitud al recurso remoto con encabezados y parámetros
        response = requests.get(
            'https://www.datos.gov.co/resource/9p2j-nzed',
            headers=headers
        )

        data = response.json()
        return jsonify(data)
    except Exception as e:
        print(f"Error al realizar la solicitud: {str(e)}")
        return jsonify({"error": "Error interno del servidor"}), 500

if __name__ == '__main__':
    app.run(port=5001)