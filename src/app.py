from flask import Flask, render_template, request, redirect, url_for
import os
import database as db

template_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=template_dir)
app.config['SUBIR ARCHIVO'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'assets')

@app.route('/')
def home():
    cursor = db.database.cursor()
    cursor.execute("SELECT * FROM juegos")
    media_list = cursor.fetchall()

    media_objects = []
    column_names = [column[0] for column in cursor.description]
    for record in media_list:
        media_objects.append(dict(zip(column_names, record)))
    cursor.close()
    return render_template('index.html', media=media_objects)

@app.route('/add')
def add_form():
    return render_template('add.html')


#Agregar juego
@app.route('/add_media', methods=['POST'])
def add_media():
    título = request.form['título']
    fecha = request.form['fecha']
    descripción = request.form['descripción']
    poster = request.files['poster']

    if poster.filename != '':
        filename = poster.filename
        poster_path = os.path.join(app.config['SUBIR ARCHIVO'], filename)
        poster.save(poster_path)
        poster = url_for('static', filename=f'assets/{filename}')
    else:
        poster = None

    if título and fecha and descripción:
        cursor = db.database.cursor()
        sql = "INSERT INTO juegos (título, fecha, descripción, poster) VALUES (%s, %s, %s, %s)"
        data = (título, fecha, descripción, poster)
        cursor.execute(sql, data)
        db.database.commit()
        cursor.close()
    return redirect(url_for('home'))

@app.route('/edit/<int:id>')
def edit_form(id):
    cursor = db.database.cursor()
    cursor.execute("SELECT * FROM juegos WHERE id = %s", (id,))
    record = cursor.fetchone()
    cursor.close()
    
    if record:
        column_names = [column[0] for column in cursor.description]
        medium = dict(zip(column_names, record))
    else:
        medium = None
    
    return render_template('edit.html', medium=medium)


#Editar juego
@app.route('/edit_media/<int:id>', methods=['POST'])
def edit_media(id):
    título = request.form['título']
    fecha = request.form['fecha']
    descripción = request.form['descripción']
    poster = request.files['poster']

    if poster.filename != '':
        filename = poster.filename
        poster_path = os.path.join(app.config['SUBIR ARCHIVO'], filename)
        poster.save(poster_path)
        poster = url_for('static', filename=f'assets/{filename}')
    else:
        poster = request.form['current_poster']

    cursor = db.database.cursor()
    sql = "UPDATE juegos SET título = %s, fecha = %s, descripción = %s, poster = %s WHERE id = %s"
    data = (título, fecha, descripción, poster, id)
    cursor.execute(sql, data)
    db.database.commit()
    cursor.close()
    return redirect(url_for('home'))

#Eliminar Juego
@app.route('/delete/<int:id>')
def delete_media(id):
    cursor = db.database.cursor()
    cursor.execute("DELETE FROM videojuegos WHERE id = %s", (id,))
    db.database.commit()
    cursor.close()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)

