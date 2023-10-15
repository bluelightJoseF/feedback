from app import app
from flaskext.mysql import MySQL
mysql=MySQL()
SECRET_KEY=b'REDACTED'#key_temporal#CHANGETHIS
SALT='0a2QzbjQK0'
app.config['MYSQL_DATABASE_USER'] = 'db_admin'
app.config['MYSQL_DATABASE_PASSWORD'] = 'REDACTED'#CHANGETHIS
app.config['MYSQL_DATABASE_DB'] = 'mydb'
app.config['MYSQL_DATABASE_HOST'] = 'admin.bluelightconsulting.tech:330666'
mysql.init_app(app)

app.config['CORS_HEADERS'] = "Content-Type"
app.config['CORS_RESOURCES'] = {r"/*": {"origins": "*"}}


