from flask import Flask
from flask_mysqldb import MySQL
from pymysql import cursors
import mimetypes

app = Flask(__name__)


app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'ardi32145'
app.config['MYSQL_DB'] = 'websitedishub'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
app.secret_key = 'ardi_key'
mysql = MySQL(app)

mimetypes.add_type('application/javascript', '.mjs')
mimetypes.add_type('text/javascript', '.js')

from vechile_counter import routes