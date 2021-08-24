from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
# Load environment variables
secretKey = os.environ.get("SECRET_KEY")
sqliteDb = os.environ.get("SQLITE_DB")

# Configure secret key
app.config["SECRET_KEY"] = secretKey

# Configure DB
dbBasedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(dbBasedir, sqliteDb)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Software info
softwareVersion = "1.0.1"

bcrypt = Bcrypt(app)
db = SQLAlchemy(app)

import models
# Create all tables
db.create_all()