from flask import request, jsonify, make_response
from waitress import serve
import jwt
import json
from functools import wraps
from init_app import app, db, bcrypt, softwareVersion, secretKey
from db_interface import *
from auth import *

auth = Auth(db, bcrypt, secretKey)
dbInterface = DbInterface(db)

# Login required decorator
#
def token_required(f):
  @wraps(f)
  def decorator(*args, **kwargs):

    token = None
    if "x-access-tokens" in request.headers:
      token = request.headers["x-access-tokens"]

    if not token:
      error = "Error: a valid token is missing"
      return make_response(jsonify({"message" : error}), 401)

    try:
      data = jwt.decode(token, app.config["SECRET_KEY"], algorithms=["HS256"])
      current_user = User.query.filter_by(email = data["email"]).first()
    except:
      error = "Error: token is invalid"
      return make_response(jsonify({"message" : error}), 401)

    return f(current_user, *args, **kwargs)
  return decorator

# Routes
#
@app.route("/", methods = ["GET"])
def home():
  # Display API version
  return jsonify({"API version": softwareVersion})

@app.route("/register", methods = ["POST"])
def register():
  data = request.get_json()
  (retcodeOk, message) = auth.register(data)
  return jsonify({"message": message})

@app.route("/login", methods = ["POST"])
def login(): 
  data = request.get_json()
  (token, retcodeOk, message) = auth.login(data)
  if retcodeOk:
    return jsonify({"token" : token})
  return make_response(jsonify({"message" : message}), 400, {"WWW.Authentication": 'Basic realm: "login required"'})

@app.route("/users", methods = ["GET"])
def users():
  user_id = request.args.get("user_id")

  if user_id != None:
    try:
      user_id = int(user_id)
    except:
      error = "Error: no such user"
      return make_response(jsonify({"message" : error}), 404)
  else:
    user_id = 0

  if request.method == "GET":
    if user_id > 0:
      (data, retcodeOk, message) = DbInterface.getUser(user_id)
      if retcodeOk:
        return jsonify(data)
      return make_response(jsonify({"message" : message}), 404)
    # Get all users
    (data, retcodeOk, message) = DbInterface.getUsers()
    if retcodeOk:
      return jsonify(data)
    return jsonify({"message" : message})

@app.route("/contacts", methods = ["GET", "POST", "PUT", "DELETE"])
@token_required
def contacts(current_user):
  contact_id = request.args.get("contact_id")

  if contact_id != None:
    try:
      contact_id = int(contact_id)
    except:
      error = "Error: no such contact"
      return make_response(jsonify({"message" : error}), 404)
  else:
    contact_id = 0

  globally = request.args.get("globally")

  if globally != None:
    globally = globally.lower() == "true"
  else:
    globally = False

  if current_user != None:
    if request.method == "GET":
      if contact_id > 0:
        (data, retcodeOk, message) = DbInterface.getContact(contact_id)
        if retcodeOk:
          return jsonify(data)
        return make_response(jsonify({"message" : message}), 404)
      if globally:
        # Get all contacts for this user regardless
        (data, retcodeOk, message) = DbInterface.getContacts(current_user.id)
        if retcodeOk:
          return jsonify(data)
        return make_response(jsonify({"message" : message}), 404)
      # Get all unique contacts across all address books
      (data, retcodeOk, message) = DbInterface.getContactsInAllAddressBooks(current_user.id)
      if retcodeOk:
        return jsonify(data)
      return make_response(jsonify({"message" : message}), 404)

    elif request.method == "POST":
      # Create a new user
      data = request.get_json()
      if not "name" in data or \
        not "surname" in data or \
        not "phone" in data:
        error = "Error: wrong parameters"
        return make_response(jsonify({"message" : error}), 404)
      (retcodeOk, message) = dbInterface.createContact(userId=current_user.id, name=data["name"], \
                            surname=data["surname"], phoneNumber=data["phone"])
      return jsonify({"message" : message})

    elif request.method == "PUT":
      if contact_id > 0:
        (data, retcodeOk, message) = DbInterface.getContact(contact_id)
        if retcodeOk:
          request_data = request.get_json()
          name = request_data["name"] if "name" in request_data else data["name"]
          surname = request_data["surname"] if "surname" in request_data else data["surname"]
          surname = request_data["surname"] if "surname" in request_data else data["surname"]
          phone = request_data["phone"] if "phone" in request_data else data["phone"]
          (retcodeOk, message) = dbInterface.updateContact(data["id"], name, surname, phone)
          return jsonify({"message" : message})
        return make_response(jsonify({"message" : message}), 404)
      error = "Error: wrong parameters"
      return make_response(jsonify({"message" : error}), 404)

    elif request.method == "DELETE":
      if contact_id > 0:
        (data, retcodeOk, message) = DbInterface.getContact(contact_id)
        if retcodeOk:
          (retcodeOk, message) = dbInterface.deleteContact(data["id"])
          return jsonify({"message" : message})
        return make_response(jsonify({"message" : message}), 404)
      error = "Error: wrong parameters"
      return make_response(jsonify({"message" : error}), 404)
  else:
    error = "Error: user not authorized"
    return make_response(jsonify({"message" : error}), 401)

@app.route("/address_books", methods = ["GET", "POST", "PUT", "DELETE"])
@token_required
def address_books(current_user):
  address_book_id = request.args.get("address_book_id")

  if address_book_id != None:
    try:
      address_book_id = int(address_book_id)
    except:
      error = "Error: no such address book"
      return make_response(jsonify({"message" : error}), 404)
  else:
    address_book_id = 0

  title = request.args.get("title")

  if title == None:
    title = ""

  if current_user != None:
    if request.method == "GET":
      if address_book_id > 0:
        (data, retcodeOk, message) = DbInterface.getAddressBook(address_book_id)
        if retcodeOk:
          return jsonify(data)
        return make_response(jsonify({"message" : message}), 404)
      # Get all address books
      (data, retcodeOk, message) = DbInterface.getAddressBooks(current_user.id)
      if retcodeOk:
        return jsonify(data)
      return make_response(jsonify({"message" : message}), 404)

    elif request.method == "POST":
      # Create a new address book
      if title:
        (retcodeOk, message) = dbInterface.createAddressBook(current_user.id, title)
        return jsonify({"message" : message})
      error = "Error: wrong parameters"
      return make_response(jsonify({"message" : error}), 404)

    elif request.method == "PUT":
      if address_book_id > 0:
        if title:
          (retcodeOk, message) = dbInterface.updateAddressBook(address_book_id, title)          
          if retcodeOk:
            return jsonify({"message" : message})
          return make_response(jsonify({"message" : message}), 404)
        error = "Error: wrong parameters"
        return make_response(jsonify({"message" : error}), 404)         
      error = "Error: wrong parameters"
      return make_response(jsonify({"message" : error}), 404)

    elif request.method == "DELETE":
      # Delete address book
      if address_book_id > 0:
        (retcodeOk, message) = dbInterface.deleteAddressBook(address_book_id)
        return jsonify({"message" : message})
      error = "Error: wrong parameters"
      return make_response(jsonify({"message" : error}), 404)
  else:
    error = "Error: user not authorized"
    return make_response(jsonify({"message" : error}), 401)

@app.route("/address_book/contacts", methods = ["GET", "POST", "DELETE"])
@token_required
def address_book_contacts(current_user):
  contact_id = request.args.get("contact_id")

  if contact_id != None:
    try:
      contact_id = int(contact_id)
    except:
      error = "Error: no such contact"
      return make_response(jsonify({"message" : error}), 404)
  else:
    contact_id = 0

  address_book_id = request.args.get("address_book_id")

  if address_book_id != None:
    try:
      address_book_id = int(address_book_id)
    except:
      error = "Error: no such address book"
      return make_response(jsonify({"message" : error}), 404)
  else:
    address_book_id = 0

  if current_user != None:
    if request.method == "GET":
      if address_book_id > 0:
        # Get all contacts in this address book
        (data, retcodeOk, message) = DbInterface.getContactsByAddressBook(address_book_id)
        if retcodeOk:
          return jsonify(data)
        return jsonify({"message" : message})
      error = "Error: wrong parameters"
      return make_response(jsonify({"message" : error}), 404)

    elif request.method == "POST":
      if address_book_id and contact_id:
        # Add contact to address book
        (retcodeOk, message) = dbInterface.addContactToAddressBook(current_user.id, address_book_id, contact_id)
        return jsonify({"message" : message})
      error = "Error: wrong parameters"
      return make_response(jsonify({"message" : error}), 404)
      
    elif request.method == "DELETE":
      if address_book_id and contact_id:
        # Delete contact from address book
        (retcodeOk, message) = dbInterface.removeContactFromAddressBook(address_book_id, contact_id)
        return jsonify({"message" : message})
      error = "Error: wrong parameters"
      return make_response(jsonify({"message" : error}), 404)
  else:
    error = "Error: user not authorized"
    return make_response(jsonify({"message" : error}), 401)

# if __name__ == "__main__":
#   app.run(debug=True)
def create_app():
    return app