from flask import Flask
from flask_mysqldb import MySQL, MySQLdb
app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'ardi32145'
app.config['MYSQL_DB'] = 'websitedishub'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

from dishubweb import routes