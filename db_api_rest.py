from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson import ObjectId

app = Flask(__name__)

# Conectar a la base de datos MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['recetas_db']
recetas_collection = db['recetas']

# Función para agregar una nueva receta
def agregar_receta(nombre, ingredientes, pasos):
    nueva_receta = {
        'nombre': nombre,
        'ingredientes': ingredientes.split(','),
        'pasos': pasos
    }
    recetas_collection.insert_one(nueva_receta)

# Función para actualizar una receta existente
def actualizar_receta(id_receta, nombre, ingredientes, pasos):
    recetas_collection.update_one({'_id': ObjectId(id_receta)}, {'$set': {'nombre': nombre, 'ingredientes': ingredientes.split(','), 'pasos': pasos}})

# Función para eliminar una receta existente
def eliminar_receta(id_receta):
    recetas_collection.delete_one({'_id': ObjectId(id_receta)})

# Función para obtener todas las recetas
def obtener_recetas():
    return recetas_collection.find()

# Rutas de la aplicación Flask
@app.route('/')
def index():
    recetas = obtener_recetas()
    return render_template('index.html', recetas=recetas)

@app.route('/agregar', methods=['POST'])
def agregar():
    nombre = request.form['nombre']
    ingredientes = request.form['ingredientes']
    pasos = request.form['pasos']
    agregar_receta(nombre, ingredientes, pasos)
    return redirect(url_for('index'))

@app.route('/actualizar/<id>', methods=['POST'])
def actualizar(id):
    nombre = request.form['nombre']
    ingredientes = request.form['ingredientes']
    pasos = request.form['pasos']
    actualizar_receta(id, nombre, ingredientes, pasos)
    return redirect(url_for('index'))

@app.route('/eliminar/<id>')
def eliminar(id):
    eliminar_receta(id)
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)
