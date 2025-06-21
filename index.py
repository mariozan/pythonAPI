import sqlite3
from flask import Flask, request, jsonify

app = Flask(__name__)

# Pruebas API
@app.route('/hello/<name>', methods=['GET']) # Path parameter
def hello(name):
    return f"Hola {name} desde Flask!"

@app.route('/', methods=['GET'])
def test():
    return jsonify({"message": "¡API Funcionando!"})

@app.route('/filtro', methods=['GET'])
def filtro():
    city = request.args.get('city')  # Query parameter
    department = request.args.get('department')  # Query parameter
    # Agregar 2 parametros mas
    return jsonify({
        "message": "Filtro aplicado!",
        "city": city,
        "department": department
    })

@app.route('/enviar', methods=['POST'])
def enviar():
    data = request.json # Body parameter
    # Aquí puedes implementar la lógica para procesar los datos recibidos
    return jsonify({"message": "Datos recibidos!", "data": data})

#------------------------------------------------#
# Base de datos
def init_db():
    with sqlite3.connect('database.db') as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                age INTEGER NOT NULL
            )
        """)
        conn.commit()

# WS Agregar usuario
@app.route('/users', methods=['POST'])
def add_user():
    data = request.json
    name = data.get('name')
    email = data.get('email')
    age = data.get('age')

    with sqlite3.connect('database.db') as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO users (name, email, age) VALUES (?, ?, ?)
        """, (name, email, age))
        conn.commit()
    
    user = {"id": cursor.lastrowid, "name": name, "email": email, "age": age}        
    return jsonify({"message": "Usuario agregado exitosamente!", "user": user}), 201

# WS Obtener todos los usuarios
@app.route('/users', methods=['GET'])
def get_users():
    with sqlite3.connect('database.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()
    
    data = [{"id": user[0], "name": user[1], "email": user[2], "age": user[3]} for user in users]
    return jsonify(data)

# WS Obtener usuario por ID
@app.route('/users/<int:user_id>', methods=['GET'])
def get_user_by_id(user_id):
    with sqlite3.connect('database.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        user = cursor.fetchone()

    if user:
        data = {"id": user[0], "name": user[1], "email": user[2], "age": user[3]}
        return jsonify(data)
    else:
        return jsonify({"message": "Usuario no encontrado"}), 404

# WS Actualizar usuario
@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.json
    name = data.get('name')
    email = data.get('email')
    age = data.get('age')
    
    with sqlite3.connect('database.db') as conn:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE users SET name = ?, email = ?, age = ? WHERE id = ?
        """, (name, email, age, user_id))
        conn.commit()
    
    user = {"id": user_id, "name": name, "email": email, "age": age}
    return jsonify({"message": "Usuario actualizado exitosamente!", "user": user}), 200

# WS Eliminar usuario
@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    with sqlite3.connect('database.db') as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
        conn.commit()

    return jsonify({"message": "Usuario eliminado exitosamente!"}), 200

if __name__ == '__main__':
    init_db()
    app.run(debug=True)