from flask import Flask
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['SECRET_KEY'] = 'ardi'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'ardi32145'
app.config['MYSQL_DB'] = 'websitedishub'

mysql = MySQL(app)

# cur = mysql.connection.cursor()

from vechile_counter import routes