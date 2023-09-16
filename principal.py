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

@programa.route('/deportistas')
def deportistas():
    return render_template("todos.html")


@programa.route('/registrar')
def registrar():
    return render_template("registrar.html")


@programa.route('/todos')
def todos():
    return render_template("todos.html")

#interfas de todos los deportistas y agregar


@programa.route('/guardardepor', methods=['POST'])
def guardardepor():
    id = request.form['id']
    nombre = request.form['nombre']
    estatura = request.form['estatura']
    peso = request.form['peso']
    fecha_naci = request.form['fecha_naci']
    foto = request.files['foto']
    ahora = datetime.now()
    nombre,fextension = os.path.splitext(foto.filename)
    nombrefoto = "A"+ahora.strftime("%Y%m%d%H%M%S")+fextension
    print(foto.filename,nombrefoto)
    foto.save("uploads/"+nombrefoto)  
    misdeportistas.agregar([id,nombre,estatura,peso,fecha_naci,foto])  
    return redirect('/todos')

    
    
    
if __name__=='__main__':
    programa.run(host='0.0.0.0', debug = True,port= 5080)