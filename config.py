from app import app
from flaskext.mysql import MySQL
mysql=MySQL()
SECRET_KEY=b'secret'#key_temporal
app.config['MYSQL_DATABASE_USER'] = 'db_admin'
app.config['MYSQL_DATABASE_PASSWORD'] = 'secret'
app.config['MYSQL_DATABASE_DB'] = 'mydb'
app.config['MYSQL_DATABASE_HOST'] = 'db:33066'
mysql.init_app(app)

app.config['CORS_HEADERS'] = "Content-Type"
app.config['CORS_RESOURCES'] = {r"/*": {"origins": "*"}}


