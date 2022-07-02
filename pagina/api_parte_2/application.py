"""application."""
from flask import Flask
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from flask import jsonify
from jwt   import encode, decode
from jwt import exceptions
from os    import getenv


import mysql.connector

app = Flask(__name__)
cnn = mysql.connector.connect(
    host="localhost", user="root", passwd="72781951", database="pagina"
)

#TOKEN = "799945fb-0363-4ff4-8c67-86720f3325d3"

def write_token(data:dict):
    token = encode(payload={**data}, key=getenv("SECRET"), algorithm="HS256")
    return token.encode("UTF-8")

AllUsers=[]
Credencial=[]
AllProducts=[]

@app.route("/")
def inicio():
    """Funcion para el inicio."""
    return render_template("inicio.html")


@app.route("/register", methods=["POST", "GET"])
def register():
    """Funcion para el register."""
    email = request.form.get("email")
    contrasena = request.form.get("contrasena")
    contrasena2 = request.form.get("contrasena2")

    if request.form.get("contrasena") == request.form.get("contrasena2"):
        cur = cnn.cursor()
        sql = "INSERT INTO usuarios (Username, Password) VALUE('{}','{}') ".format(
            email, contrasena
        )
        cur.execute(sql)
        cnn.commit()
        cur.close()
        if request.method == "POST":
            return redirect(url_for("login"))
        else:
            return render_template("Register.html")
    return render_template("Register.html")



@app.route("/login", methods=["POST", "GET"])
def login():
  return render_template("login2.html")

@app.route("/logueado", methods=["POST"])
def logueando():
  email = request.form.get("Username")
  contrasena = request.form.get("Password")
  SOS=False
  cur = cnn.cursor()
  try:
    sql="SELECT Username, Password FROM usuarios"
    cur.execute(sql)
    datos=cur.fetchall()
    for dato in datos:
        if dato[0]==email and dato[1]==contrasena:
            usuario={"Username":email, "Password":contrasena}
            Credencial.append(usuario)
            SOS=True
            '''TOKEN = write_token(User)
            print(TOKEN)'''
            print(Credencial)
    return jsonify({'success': SOS,'Credencial':Credencial })
  except Exception as ex:
    return jsonify({ 'success':False})
    
@app.route("/token", methods=["POST"])
def va():
  cur = cnn.cursor()
  try:
    sql="SELECT Username, Password FROM usuarios"
    cur.execute(sql)
    datos=cur.fetchall()
    for dato in datos:
        if dato[0]==email and dato[1]==contrasena:
            usuario={"Username":email, "Password":contrasena}
            Credencial.append(usuario)
            '''TOKEN = write_token(User)
            print(TOKEN)'''
            print(Credencial)
            SOS=True
        else:
            SOS=False
    return jsonify({'success': succe,'Credencial':Credencial })
    
  except Exception as ex:
    return jsonify({ 'success':False})

@app.route("/obtener/allusers", methods=["POST", "GET"])
def JSON_ALLUSERS():
  cur = cnn.cursor()
  try:
    sql="SELECT Username, Password FROM usuarios"
    cur.execute(sql)
    datos=cur.fetchall()


    for dato in datos:
      usuario={"Username":dato[0], "Password":dato[1]}
      AllUsers.append(usuario)
    return jsonify({"AllUsers":AllUsers, "mensaje":"Datos correctamente exportados CON JSON"})

  except Exception as ex:
    return jsonify({ "mensaje":"ERROR"})
 



@app.route("/productos")
def productos():
    """Funcion para el productos."""
    return render_template("productos.html")


@app.route("/cart")
def cart():
    """Funcion para el cart."""
    return render_template("Cart.html")


@app.route("/register_product", methods=["POST", "GET"])
def register_product():
    """Funcion para el register_product."""
    namepro = request.form.get("namepro")
    precio = request.form.get("precio")
    nombreimg = request.form.get("nombreimg")
    descripcion = request.form.get("descripcion")
    curs = cnn.cursor()
    sql = "INSERT INTO productos (Nombre, Precio, Url, Descrip) VALUE('{}','{}','{}','{}') ".format(
        namepro, precio, nombreimg, descripcion
    )
    curs.execute(sql)
    cnn.commit()
    curs.close()
    if request.method == "POST":
        return redirect(url_for("productos"))
    else:
        return render_template("Register_Pro.html")



@app.route("/obtener/allproducts", methods=["POST", "GET"])
def JSON_ALLPRODUCTS():
  cur = cnn.cursor()
  try:
    sql="SELECT Nombre, Precio, Url, Descrip FROM productos"
    cur.execute(sql)
    datos=cur.fetchall()


    for dato in datos:
      producto={"Nombre":dato[0], "Precio":dato[1], "Url":dato[2], "descripcion":dato[3]}
      AllProducts.append(producto)
    return jsonify({"AllProducts":AllProducts, "mensaje":"Datos correctamente exportados CON JSON"})

  except Exception as ex:
    return jsonify({ "mensaje":"ERROR"})
 

@app.route("/redes")
def redes():
    """Funcion para el redes."""
    return render_template("redes.html")


@app.route("/pago")
def pago():
    """Funcion para el pago."""
    return render_template("pago.html")


if __name__ == "__main__":
    app.run(debug=True)
