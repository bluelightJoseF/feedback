from flask import Flask, request
from lxml import etree
import traceback
import json
from functools import cached_property, wraps
from app import app
from flask import json, jsonify
from flask import request
from Crypto.PublicKey import RSA
import os
from Crypto.Util.number import long_to_bytes
import datetime
import jwt
from flaskext.mysql import MySQL
from config import SECRET_KEY
from config import mysql

def token_required(f):
	@wraps(f,)
	def decorated(*args, **kwargs):
		if 'Authorization' in request.headers:
			token = request.headers['Authorization']
			print (token)
		if not 'Authorization' in request.headers:
			return jsonify({'message':'Error no Token Header'},403)

		if not token:
			return jsonify({'message' : 'No Token'}), 403
		try: 
			data = jwt.decode(token,SECRET_KEY,algorithms=["HS256"])
		except:
			return jsonify({'message' : 'Token invalido!'}, 403)
		return f(data,*args, **kwargs)
	return decorated

@app.route('/dashboard', methods=['GET'])
@token_required
def dash(data):
    if data["rol"]== "admin": 
        print (data)
        return """
    <html>
    <head><title>Admin Dashboard DEV</title></head>
    <body>
        <p><h3>Login Exitoso!!! Bienvenido Admin...</h3></p>
        <a href="/rest">Revisar comentarios</a><br>
    </body>
    </html>
    """
    else:
          return """
    <html>
    <head><title>Admin Dashboard DEV</title></head>
    <body>
        <p><h3>No has iniciado sesion como admin</h3></p>
    </body>
    </html>
    """
     
@app.route('/admin', methods=['GET', 'POST'])
def login_admin():
    if request.method == 'GET':
        access_token = jwt.encode({'rol':'invitado','nombre':'public', 'exp': datetime.datetime.utcnow()+datetime.timedelta(minutes=1200)},SECRET_KEY,algorithm="HS256")
        respone = jsonify({'message':'Login Anonimo exitoso, Set Header: Authorization','value': access_token })
        respone.status_code = 200
        return respone


    if request.method == 'POST':
		# Create variables for easy access
        _json = request.json
        _user=_json['username']
        _pass=_json['password']
        _rol=0
        #conn = mysql.connect()
        #cursor = conn.cursor()
        #cursor.execute('SELECT id_usuario, nombre, apellidos FROM usuario WHERE correo = %s AND password = %s', (_user, _pass))
        #account = cursor.fetchone()
        #cursor = conn.cursor()
        #cursor.close() 
        #conn.close()
		#print(_hashdigest)
        print(_json)
        if (_user=="admin" and _pass =="Password123" ):
			#print(type(account))
            _nom="Jose"+'Antonio'
            if _json:
                access_token = jwt.encode({'id_usuario':'0001','rol':'admin','nombre':_nom, 'exp': datetime.datetime.utcnow()+datetime.timedelta(minutes=1200)},SECRET_KEY,algorithm="HS256")
                respone = jsonify({'message':'Login Exitoso!','token': access_token })
                respone.status_code = 200
                return respone
            else:
                respone =jsonify({'message':'Incorrect username/password!'})
                respone.status_code=404
                return respone
        else:
            respone =jsonify({'message':'Usuario incorrecto/Usuario no registrado'})
            respone.status_code=403
            return respone



@app.route('/')
def index():
    return """
    <html>
    <head><title>Feedback DEV</title></head>
    <body>
        <p><h3>Entra aqui para dejar tus comentarios</h3></p>
        <a href="/rest">Deja tu comentario</a><br>
    </body>
    </html>
    """

@app.route('/rest', methods=['POST', 'GET'])
def xml():
    parsed_xml = None

    html = """
    <html>
      <body>
    """

    if request.method == 'POST':
        xml = request.form['comment']
        parser = etree.XMLParser(no_network=False)
        try:
            doc = etree.fromstring(str(xml), parser)
            parsed_xml = etree.tostring(doc)
            #print(repr(parsed_xml))
        except:
            print("Cannot parse the xml")
            html += "Error:\n<br>\n" + traceback.format_exc()
    if (parsed_xml):
        html += "Respuesta:\n<br>\n" + parsed_xml.decode()
    else:
        html += """
	  <form action = "/rest" method = "POST">
		 <p><h3>Deja aqui tu comentario!</h3></p>
		 <textarea class="input" name="comment" cols="40" rows="5"></textarea>
		 <p><input type = 'submit' value = 'enviar'/></p>
	  </form>
	"""

    html += """
      </body>
    </html>
    """

    return html


if __name__ == '__main__':
    app.run(debug=False, port=4441, host='0.0.0.0')
