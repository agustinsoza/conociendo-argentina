from flask import Flask, render_template, request, redirect, url_for, send_from_directory, flash, session
from flask_mysqldb import MySQL
# from pymysql.cursors import DictCursor
from datetime import datetime
import os

app = Flask(__name__)
mysql = MySQL()

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'conociendo_argentina'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
app.config['SECRET_KEY'] = 'codoacodo'

UPLOADS = os.path.join('src/uploads')
app.config['UPLOADS'] = UPLOADS #Guardamos la ruta como un valor en la app

PROVINCIAS = os.path.join('src/templates/auth/provincias')
app.config['PROVINCIAS'] = PROVINCIAS

mysql.init_app(app)

@app.route('/userpic/<nombreFoto>')
def userpic(nombreFoto):
    return send_from_directory(os.path.join('uploads'), nombreFoto)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/registro', methods=["GET", "POST"])
def registro():

    conn = mysql.connection
    cur = conn.cursor()

    if request.method == "GET":
        return render_template('registro.html')
    else:

        _usuario = request.form['usuario']
        _nombre = request.form['nombre']
        _apellido = request.form['apellido']
        _correo = request.form['correo']
        _pwd = request.form['pwd']
        _pwd2 = request.form['pwd2']
        _cumpleaños = request.form['birthdate']
        _sexo = request.form['gender']
        _provincia = request.form['province']
        _localidad = request.form['city']

        if _usuario == '' or _nombre == '' or _apellido == '' or _correo == '' or _pwd == '' or _pwd2 == '':
            flash(' Debe completar los campos obligatorios! ')
            return redirect(url_for('registro'))
        else:
            sql_create = "INSERT INTO usuarios (Nombres, Apellidos, Usuario, Correo_Electronico, Contraseña, Fecha_Nac, Sexo, Provincia, Localidad) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);"
            datos = (_nombre, _apellido, _usuario, _correo, _pwd, _cumpleaños, _sexo, _provincia, _localidad)

            cur.execute(sql_create, datos)
            conn.commit()
            cur.close()

            flash(' Registrado Correctamente! ', 'formulario_registro-check')
            return redirect('/acceder')

@app.route('/terminos')
def terminos():
    return render_template('terminos.html')

@app.route('/acceder', methods=['GET', 'POST'])
def acceder():
    conn = mysql.connection
    cur = conn.cursor()

    if request.method == 'POST':

        _user = request.form['user']
        _pwd = request.form['pwd']
        
        sql = f'SELECT * FROM usuarios WHERE Usuario = "{_user}" OR Correo_Electronico = "{_user}" AND Contraseña = "{_pwd}"'
        cur.execute(sql)
        conn.commit()
        user_log = cur.fetchone()
        cur.close()

        if user_log:
                session['user'] = user_log
                return redirect(url_for('home'))     
        else:
            flash(' El usuario ingresado no existe! ', 'formulario_registro-error')
            return redirect(url_for('acceder'))
    else:
        return render_template('acceder.html')

    
# INICIO DE RUTAS PARA USUARIOS LOGUEADOS
    
@app.route('/home')
def home():
    if 'user' in session:
        return render_template('auth/home.html')
    else:
        return redirect('/acceder')

@app.route('/perfil')
def perfil():
    if 'user' in session:
        usuario = session['user']
        return render_template('auth/perfil.html', usuario=usuario)
    else:
        return redirect('/acceder')

@app.route('/auth/provincias/<nombreProvincia>')
def provincias(nombreProvincia):
    if 'user' in session:
        Header = {
            'buenos_aires' : ' Buenos Aires',
            'catamarca' : ' Catamarca',
            'chaco' : ' Chaco',
            'chubut' : ' Chubut',
            'cordoba' : ' Córdoba',
            'corrientes' : ' Corrientes',
            'entre_rios' : ' Entre Ríos',
            'formosa' : ' Formosa',
            'jujuy' : ' Jujuy',
            'la_pampa' : ' La Pampa',
            'la_rioja' : ' La Rioja',
            'mendoza' : ' Mendoza',
            'misiones' : ' Misiones',
            'neuquen' : ' Neuquen',
            'rio_negro' : ' Río Negro',
            'salta' : ' Salta',
            'san_juan' : ' San Juan',
            'san_luis' : ' San Luis',
            'santa_cruz' : ' Santa Cruz',
            'santa_fe' : ' Santa Fe',
            's_del_estero' : ' Santiago del Estero',
            'tierra_del_fuego' : ' Tierra del Fuego',
            'tucuman' : ' Tucuman'
        }
        Titulo = {
            'buenos_aires' : 'Buenos Aires',
            'catamarca' : 'Catamarca',
            'chaco' : 'Chaco',
            'chubut' : 'Chubut',
            'cordoba' : 'Córdoba',
            'corrientes' : 'Corrientes',
            'entre_rios' : 'Entre Ríos',
            'formosa' : 'Formosa',
            'jujuy' : 'Jujuy',
            'la_pampa' : 'La Pampa',
            'la_rioja' : 'La Rioja',
            'mendoza' : 'Mendoza',
            'misiones' : 'Misiones',
            'neuquen' : 'Neuquen',
            'rio_negro' : 'Río Negro',
            'salta' : 'Salta',
            'san_juan' : 'San Juan',
            'san_luis' : 'San Luis',
            'santa_cruz' : 'Santa Cruz',
            'santa_fe' : 'Santa Fe',
            's_del_estero' : 'Santiago del Estero',
            'tierra_del_fuego' : 'Tierra del Fuego',
            'tucuman' : 'Tucuman'
        }

        if nombreProvincia in Header:
            return render_template(f'auth/provincias/{nombreProvincia}.html',header=Header[nombreProvincia], titulo=Titulo[nombreProvincia], imagen=nombreProvincia)
        else:
            return '<h1>Page not found</h1>', 404
    else:
        return redirect('/acceder')

@app.route('/modify/<id>')
def modify(id):
    sql_modify = "SELECT * FROM usuarios WHERE id_Usuario=%s;"

    conn = mysql.connection
    cur = conn.cursor()
    cur.execute(sql_modify, id)
    usuario = cur.fetchone()
    conn.commit()

    cur.close()

    return render_template('Usuarios/edit.html', usuario=usuario)

@app.route('/update', methods=["POST"])
def update():
    if 'user' in session:
        if request.method == 'POST':

            _id = request.form['ID']
            _usuario = request.form['usuario']
            _nombre = request.form['nombre']
            _apellido = request.form['apellido']
            _correo = request.form['correo']
            _pwd = request.form['pwd']
            _pwd2 = request.form['pwd2']
            _cumpleaños = request.form['birthdate']
            _sexo = request.form['gender']
            _provincia = request.form['province']
            _localidad = request.form['city']
            # _foto = request.files['Foto']
            now = datetime.now()
            tiempo = now.strftime("%Y%H%M%S")

            print(_cumpleaños)

            conn = mysql.connection
            cur = conn.cursor()

            # if _foto.filename != '':
            #     nuevoNombreFoto = tiempo + '_' + _foto.filename
            #     _foto.save("src/uploads/" + nuevoNombreFoto)

            #     sql = f'SELECT Foto FROM usuarios WHERE id_Usuario = {_id}'
            #     cur.execute(sql)
            #     conn.commit()

            #     nombreFoto = cur.fetchone()
            #     borrarEstaFoto = os.path.join(app.config['UPLOADS'], nombreFoto['Foto'])

            #     try:
            #         os.remove(os.path.join(app.config['UPLOADS'], nombreFoto['Foto']))
            #     except:
            #         pass

            #     sql = f'UPDATE usuarios SET Foto = "{nuevoNombreFoto}" WHERE id_Usuario = {_id};'
            #     cur.execute(sql)
            #     conn.commit()

            if _cumpleaños == '':
                if _usuario == '' or _nombre == '' or _apellido == '' or _correo == '' or _pwd == '' or _pwd2 == '':
                    flash(' Debe completar todos los campos para actualizar ', 'formulario_registro-error')
                    return redirect('/perfil')
                else:
                    sql_update = "UPDATE usuarios SET Usuario = %s, Nombres = %s, Apellidos = %s, Correo_Electronico = %s, Contraseña = %s, Sexo = %s, Provincia = %s, Localidad = %s WHERE ID = %s"
                    datos = (_usuario, _nombre, _apellido, _correo, _pwd, _sexo, _provincia, _localidad, _id)

                    cur.execute(sql_update, datos)
                    conn.commit()

                    sql = f'SELECT * FROM usuarios WHERE ID = {_id}'
                    cur.execute(sql)
                    conn.commit()
                    user_log = cur.fetchone()
                    cur.close()
                    session['user'] = user_log
                cur.close()
                return redirect('/perfil')
            else:
                if _usuario == '' or _nombre == '' or _apellido == '' or _correo == '' or _pwd == '' or _pwd2 == '':
                    flash(' Debe completar todos los campos para actualizar ', 'formulario_registro-error')
                    return redirect('/perfil')
                else:
                    sql_update = "UPDATE usuarios SET Usuario = %s, Nombres = %s, Apellidos = %s, Correo_Electronico = %s, Contraseña = %s, Fecha_Nac = %s, Sexo = %s, Provincia = %s, Localidad = %s WHERE ID = %s"
                    datos = (_usuario, _nombre, _apellido, _correo, _pwd, _cumpleaños, _sexo, _provincia, _localidad, _id)

                    cur.execute(sql_update, datos)
                    conn.commit()

                    sql = f'SELECT * FROM usuarios WHERE ID = {_id}'
                    cur.execute(sql)
                    conn.commit()
                    user_log = cur.fetchone()
                    cur.close()
                    session['user'] = user_log
                cur.close()
                return redirect('/perfil')

    return redirect('/')
        

@app.route('/delete/<id>')
def delete(id):
    if 'user' in session:
        conn = mysql.connection
        cur = conn.cursor()

        sql_delete = f'DELETE FROM usuarios WHERE ID = {id};'

        cur.execute(sql_delete)
        conn.commit()
        cur.close()

        return redirect('/acceder')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/acceder')

if __name__ == '__main__':
    app.run(debug=True)