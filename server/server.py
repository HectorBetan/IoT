from flask import Flask, jsonify, request
from pymongo import MongoClient

app = Flask(__name__)

# Conexión a la base de datos de MongoDB
client = MongoClient('mongodb+srv://hectorbetancourt1992:DnfbYxm0wmQ9IHrM@cluster0.ag7ggc4.mongodb.net/?retryWrites=true&w=majority')
db = client['air-quality']  # Reemplaza con el nombre de tu base de datos
collection = db['sensores']  # Reemplaza con el nombre de tu colección

# Endpoint para obtener los últimos x datos de la base de datos
@app.route('/get_last_data', methods=['GET'])
def get_last_data():
    try:
        # Obtener el parámetro 'x' del request, si no se proporciona, se establecerá en 10 por defecto
        x = int(request.args.get('x', 10))

        # Obtener los últimos x documentos de la colección
        data = list(collection.find().sort("_id", -1).limit(x))
        
        # Devolver los datos en formato JSON
        return jsonify(data)
    except Exception as e:
        print(f"Error al obtener los datos de la base de datos: {str(e)}")
        return jsonify({"error": "Error interno del servidor"}), 500

# Endpoint para agregar datos sobre calidad del aire a la base de datos
@app.route('/post_data', methods=['POST'])
def post_data():
    try:
        # Obtener los datos del cuerpo del request
        data = request.json
        print(data)
        # Insertar los datos en la colección
        result = collection.insert_one(data)

        # Devolver el ID del documento insertado
        return jsonify({"inserted_id": str(result.inserted_id)})
    except Exception as e:
        print(f"Error al insertar datos en la base de datos: {str(e)}")
        return jsonify({"error": "Error interno del servidor"}), 500

if __name__ == '__main__':
    app.run(port=5001)