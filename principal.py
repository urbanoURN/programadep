from datetime import datetime
import os
from flask import Flask, redirect, render_template, request, send_from_directory
from flaskext.mysql import MySQL
from clases import Deportistas

programa = Flask(__name__)
bdd = MySQL()

programa.config['MYSQL_DATABASE_HOST'] ='localhost'
programa.config['MYSQL_DATABASE_PORT'] = 3306
programa.config['MYSQL_DATABASE_USER'] = 'root'
programa.config['MYSQL_DATABASE_PASSWORD'] = ''
programa.config['MYSQL_DATABASE_DB'] = 'primert'

bdd.init_app(programa)
misdeportistas = Deportistas(bdd)

#fotos
CARPETAUP = os.path.join('uploads')
programa.config['CARPETAUP']=CARPETAUP

@programa.route('/uploads/<nombre>')
def uploads(nombre):
    return send_from_directory(programa.config['CARPETAUP'],nombre)
#fotos

#interfas de todos los deportistas y agregar
@programa.route('/')
def todosdep():
    resultado = misdeportistas.consultar()
    return render_template("todos.html", res=resultado)

@programa.route('/registrar')
def registrar():
    return render_template("registrar.html", msg="")


#interfas de todos los deportistas y agregar

@programa.route('/guardardepor', methods=['POST'])
def guardardepor():
    id = request.form['id']
    nombre_dep= request.form['nombre']
    estatura = request.form['estatura']
    peso = request.form['peso']
    fecha_naci = request.form['fecha_naci']
    foto = request.files['foto']
    if misdeportistas.buscar(id):
        return render_template("registrar.html",msg="Id de deportista YA registrado")
    ahora = datetime.now()
    nombre_foto,fextension = os.path.splitext(foto.filename)
    nombreFoto = "A"+ahora.strftime("%Y%m%d%H%M%S")+fextension
    print(foto.filename,nombreFoto)
    foto.save("uploads/"+nombreFoto)  
    misdeportistas.agregar([id,nombre_dep,estatura,peso,fecha_naci,nombreFoto])  
    return redirect('/')

    
    
    
if __name__=='__main__':
    programa.run(host='0.0.0.0', debug = True,port= 5080)