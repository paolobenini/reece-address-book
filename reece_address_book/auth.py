""" This module contain the Auth class. """
import jwt
from models import *

class Auth:
  """
  This class provide methods to register and login users.
  """
  def __init__(self, db_instance, bcrypt_instance, secretKey):
    self.__db = db_instance
    self.__bcrypt = bcrypt_instance
    self.__secretKey = secretKey

  def login(self, request_data):
    """
    Login user with email and password.

    Parameters:
      request_data

    Returns:
      (token, retcodeOk, message)
    """
    retcodeOk = True
    message = ""
    token = None
    if not request_data or not "email" in request_data or not "password" in request_data:
      retcodeOk = False
      message = "Error: invalid email or password."
    else:
      user = User.query.filter_by(email = request_data["email"]).first()
      if user != None:
        if self.__bcrypt.check_password_hash(user.password, request_data["password"]):
          token = jwt.encode({"userId": user.id, "email": user.email}, self.__secretKey)
      else:
        retcodeOk = False
        message = "Error: no user with that email."
    return (token, retcodeOk, message)

  def register(self, request_data):
    """
    Register a new user with email and password.

    Parameters:
      request_data

    Returns:
      (retcodeOk, message)
    """
    retcodeOk = True
    message = "Registered successfully."
    if not "email" in request_data or \
      not "password" in request_data:
      retcodeOk = False
      message = "Error: wrong parameters"
    else:      
      user = User.query.filter_by(email = request_data["email"]).first()
      if user == None:
        hashed_password = self.__bcrypt.generate_password_hash(request_data["password"]).decode("utf-8")

        try:
          newUser = User(email = request_data["email"], password = hashed_password)
          self.__db.session.add(newUser)
          self.__db.session.commit()
        except:
          retcodeOk = False
          message = "Error: database error"
      else:
        retcodeOk = False
        message = "Error: user already exists"
    return (retcodeOk, message)
