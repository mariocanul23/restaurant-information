from flask import Flask, jsonify, request
import database as db
import uuid
import pandas as pd
import os


app = Flask(__name__)

#Rutas de la aplicación
#Ruta para guardar información de restaurantes en la BD
@app.route('/create_restaurant', methods=['POST'])
def create_restaurant():
    try:
        id = uuid.uuid4().hex
        rating = request.form['rating']
        name = request.form['name']
        site = request.form['site']
        email = request.form['email']
        phone = request.form['phone']
        street = request.form['street']
        city = request.form['city']
        state = request.form['state']
        lat = request.form['lat']
        lng = request.form['lng']

        cursor = db.database.cursor()
        sql = "INSERT INTO restaurants(id,rating, name, site, email, phone, street, city, state, lat, lng) VALUES(%s,%s, %s, %s, %s, %s, %s, %s, %s,%s, %s)"
        data = (id,rating, name, site, email, phone, street, city, state, lat, lng)
        cursor.execute(sql, data)
        db.database.commit()
        return jsonify({'message': 'Restaurant created successfully', 'data': data}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/read_restaurant')
def read_restaurant():
    cursor = db.database.cursor()
    cursor.execute("SELECT * FROM restaurants")
    myresult = cursor.fetchall()
    #Convertir los datos a diccionario
    insertObject = []
    columNames = [column[0] for column in cursor.description]
    for record in myresult:
        insertObject.append(dict(zip(columNames, record)))

    cursor.close()
    return jsonify(insertObject)

@app.route('/update_restaurant/<string:id>', methods=['PUT'])
def update_restaurant(id):
     try:
        rating = request.form['rating']
        name = request.form['name']
        site = request.form['site']
        email = request.form['email']
        phone = request.form['phone']
        street = request.form['street']
        city = request.form['city']
        state = request.form['state']
        lat = request.form['lat']
        lng = request.form['lng']

        cursor = db.database.cursor()
        sql = "UPDATE restaurants SET(rating=%s, name=%s, site=%s, email=%s, phone=%s, street=%s, city=%s, state=%s, lat=%s, lng=%s) WHERE id=%s"
        data = (rating, name, site, email, phone, street, city, state, lat, lng, id)
        cursor.execute(sql, data)
        db.database.commit()
        return jsonify({'message': 'Restaurant created successfully', 'data': data}), 200
        # return redirect(url_for('home'))
     except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/delete_restaurant/<string:id>', methods=['DELETE'])
def delete_restaurant(id):
    cursor = db.database.cursor()
    sql = "DELETE FROM restaurants WHERE id = %s"
    data = (id,)
    try:
        cursor.execute(sql, data)
        db.database.commit()
        return jsonify({'message': 'Restaurant deleted successfully', 'id': id})
    except Exception as err:
        return jsonify({'error': str(err)}), 400

@app.route('/import_csv', methods=['POST'])
def import_csv():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file and file.filename.endswith('.csv'):
        try:
            # Guarda temporalmente el archivo
            file_path = os.path.join('/tmp', file.filename)
            file.save(file_path)
            
            # Lee el archivo CSV
            df = pd.read_csv(file_path)
            
            cursor = db.database.cursor()
            
            # Itera sobre el DataFrame y realiza inserciones en la base de datos
            for _, row in df.iterrows():
                sql = "INSERT INTO restaurants (id, rating, name, site, email, phone, street, city, state, lat, lng) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                data = (row['id'], row['rating'], row['name'], row['site'], row['email'], row['phone'], row['street'], row['city'], row['state'], row['lat'], row['lng'])
                cursor.execute(sql, data)
                
            db.database.commit()
            cursor.close()
            
            # Eliminar el archivo temporal
            os.remove(file_path)
            
            return jsonify({'message': 'Restaurants imported successfully'}), 201
        
        except Exception as e:
            return jsonify({'error': str(e)}), 400
    else:
        return jsonify({'error': 'Invalid file format'}), 400


if __name__ == '__main__':
    app.run(debug=True, port=4000)