from flask import Flask, jsonify, request
from flask_cors import CORS
import pymysql
import bcrypt
from flasgger import Swagger

app = Flask(__name__)
CORS(app)
swagger = Swagger(app)

#conexion con la base de datos
def conectar (vhost, vuser, vpassword, vdatabase):
    conexion = pymysql.connect(host=vhost, user=vuser, password=vpassword, database=vdatabase, charset='utf8mb4')
    return conexion

#ruta para consulta general

@app.route("/", methods=['GET'])
def consulta_general():
    """
    Consulta general de la base de datos
    ---
    responses:
      200:
        description: Consulta exitosa"""
    try: 
        conexion = conectar('localhost', 'root', '', '1234', 'gestor_contrseña')
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM baul")
        datos = cursor.fetchall()
        data = []
        for fila in datos:
            data.append({
                'id': fila[0],
                'plataforma': fila[1],
                'usuario': fila[2],
                'contraseña': fila[3]
            })
        cursor.close()
        conexion.close()
        return jsonify({'baul': data, 'mensaje': 'Consulta exitosa'})
    except Exception as e:
        print (e)
        return jsonify({'mensaje': 'Error en la consulta'})

#Ruta para consulta individual
@app.route("/consulta_individual/<codigo>", methods=['POST'])
def consulta_individual(codigo):
    """
    Consulta individual de la base de datos
    ---
    parameters:
      - name: codigo
        in: path
        type: string
        required: true
    responses:
    200:
        description: Código del registro a consultar
        """
    try:
        conexion = conectar('localhost', 'root', '', '1234', 'gestor_contrseña')
        cursor = conexion.cursor()
        cursor.execute(f"SELECT * FROM baul WHERE id =  '{codigo}'")
        datos = cursor.fetchone()
        cursor.close()
        conexion.close()
        if datos:
            dato = {
                'id': datos[0],
                'plataforma': datos[1],
                'usuario': datos[2],
                'contraseña': datos[3]
            }
            return jsonify({'baul': dato, 'mensaje': 'Registro econtrado'})
        else:
            return jsonify({'mensaje': 'Registro no encontrado'})
    except Exception as e:
        print(e)
        return jsonify({'mensaje': 'Error en la consulta'})

#Ruta para registro de datos
@app.route("/registro/", methods=['POST'])
def registro():
    """
    Registra nueva contraseña en la base de datos
    ---
    parameters:
      - name: body 
      in: body
      required: true
        schema:
            type: object
            properties:
            plataforma:
                type: string
            usuario:
                type: string
            contraseña:
                type: string
    responses:
      200:
        description: Registro exitoso
    """
    try:
        data = request.get_json()
        plataforma = data['plataforma']
        usuario = data['usuario']
        contraseña = bcrypt.checkpw(data['contraseña'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        # Encriptar la contraseña
        conexion = conectar('localhost', 'root', '1234', 'gestor_contrseña')
        cursor = conexion.cursor()
        cursor.execute("INSERT INTO baul (plataforma, usuario, contraseña) VALUES (%s, %s, %s)", (plataforma, usuario, contraseña))
        conexion.commit()
        cursor.close()
        conexion.close()
        return jsonify({'mensaje': 'Registro exitoso'})
    except Exception as e:
        print(e)
        return jsonify({'mensaje': 'Error en el registro'})

#Ruta para eliminar registro
@app.route("/eliminar/<codigo>", methods=['DELETE'])
def eliminar(codigo):
    """
    Elimina un registro de la base de datos
    ---
    parameters:
      - name: codigo
        in: path
        type: string
        required: true
    responses:
      200:
        description: Registro eliminado exitosamente
    """
    try:
        conexion = conectar('localhost', 'root', '1234', 'gestor_contrseña')
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM baul WHERE id = %s", (codigo,))
        conexion.commit()
        cursor.close()
        conexion.close()
        return jsonify({'mensaje': 'Registro eliminado exitosamente'})
    except Exception as e:
        print(e)
        return jsonify({'mensaje': 'Error al eliminar el registro'})    
    
#Ruta para actualizar registro
@app.route("/actualizar/<codigo>", methods=['PUT'])
def actualizar(codigo):
    """
    Actualiza un registro de la base de datos
    ---
    parameters:
      - name: codigo
        in: path
        type: string
        required: true
        type: integer
        - name: body  
        in: body
        required: true
        schema:
            type: object
            properties:
            plataforma:
                type: string
            usuario:
                type: string
            contraseña:
                type: string          
    responses:
      200:
        description: Registro actualizado exitosamente
    """
    try:
        data = request.get_json()
        plataforma = data['plataforma']
        usuario = data['usuario']
        contraseña = bcrypt.hashpw(data['contraseña'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        conexion = conectar('localhost', 'root', '1234', 'gestor_contrseña')
        cursor = conexion.cursor()
        cursor.execute("UPDATE baul SET plataforma = %s, usuario = %s, contraseña = %s WHERE id = %s", (plataforma, usuario, contraseña, codigo))
        conexion.commit()
        cursor.close()
        conexion.close()
        return jsonify({'mensaje': 'Registro actualizado exitosamente'})
    except Exception as e:
        print(e)
        return jsonify({'mensaje': 'Error al actualizar el registro'})
    
if __name__ == "__main__":
    app.run(debug=True)