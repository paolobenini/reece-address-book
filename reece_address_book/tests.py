""" This module contains code for unit tests """
from flask import request, jsonify, make_response
import jwt
import json
from init_app import app, db, bcrypt, softwareVersion, secretKey
from db_interface import *
from auth import *

auth = Auth(db, bcrypt, secretKey)
dbInterface = DbInterface(db)

#
# UNIT TESTS: DbInterface class
#

#  getUser
#
# (data, retcode, message) = DbInterface.getUser(1)
# if message:
#   print(f"retcode ok = {retcode}, message = {message}")
# else:
#   print(f"retcode ok = {retcode}")
# print(json.dumps(data, indent=2))

#  getUsers
#
# (data, retcode, message) = DbInterface.getUsers()
# if message:
#   print(f"retcode ok = {retcode}, message = {message}")
# else:
#   print(f"retcode ok = {retcode}")
# print(json.dumps(data, indent=2))

# getUserByEmail
#
# (data, retcode, message) = DbInterface.getUserByEmail("paolo@fakedomain.com")
# if message:
#   print(f"retcode ok = {retcode}, message = {message}")
# else:
#   print(f"retcode ok = {retcode}")
# print(json.dumps(data, indent=2))

# getContacts
#
# (data, retcode, message) = DbInterface.getContacts(1)
# if message:
#   print(f"retcode ok = {retcode}, message = {message}")
# else:
#   print(f"retcode ok = {retcode}")
# print(json.dumps(data, indent=2))

# getContactsByFullName
#
# (data, retcode, message) = DbInterface.getContactsByFullName("jaxx", "arellano")
# if message:
#   print(f"retcode ok = {retcode}, message = {message}")
# else:
#   print(f"retcode ok = {retcode}")
# print(json.dumps(data, indent=2))

# getContactsByFirstName
#
# (data, retcode, message) = DbInterface.getContactsByFirstName("Jaxx")
# if message:
#   print(f"retcode ok = {retcode}, message = {message}")
# else:
#   print(f"retcode ok = {retcode}")
# print(json.dumps(data, indent=2))

# getContactsBySurname
#
# (data, retcode, message) = DbInterface.getContactsBySurname("Arellano")
# if message:
#   print(f"retcode ok = {retcode}, message = {message}")
# else:
#   print(f"retcode ok = {retcode}")
# print(json.dumps(data, indent=2))

# getContactsByPhone
#
# (data, retcode, message) = DbInterface.getContactsByPhone("0444612341")
# if message:
#   print(f"retcode ok = {retcode}, message = {message}")
# else:
#   print(f"retcode ok = {retcode}")
# print(json.dumps(data, indent=2))

# getContactsByAddressBook
#
# (data, retcode, message) = DbInterface.getContactsByAddressBook(1)
# if message:
#   print(f"retcode ok = {retcode}, message = {message}")
# else:
#   print(f"retcode ok = {retcode}")
# print(json.dumps(data, indent=2))

# getContact
#
# (data, retcode, message) = DbInterface.getContact(20)
# if message:
#   print(f"retcode ok = {retcode}, message = {message}")
# else:
#   print(f"retcode ok = {retcode}")
# print(json.dumps(data, indent=2))

# updateContact
#
# (retcode, message) = dbInterface.updateContact(20, "Indigo", "Wickens", "0456470374")
# if message:
#   print(f"retcode ok = {retcode}, message = {message}")
# else:
#   print(f"retcode ok = {retcode}")

# deleteContact
#
# (retcode, message) = dbInterface.deleteContact(21)
# if message:
#   print(f"retcode ok = {retcode}, message = {message}")
# else:
#   print(f"retcode ok = {retcode}")

# createContact
#
# (retcode, message) = dbInterface.createContact(1, "Paolo", "Benini", "0450777101")
# if message:
#   print(f"retcode ok = {retcode}, message = {message}")
# else:
#   print(f"retcode ok = {retcode}")

# getAddressBooks
#
# (data, retcode, message) = DbInterface.getAddressBooks(1)
# if message:
#   print(f"retcode ok = {retcode}, message = {message}")
# else:
#   print(f"retcode ok = {retcode}")
# print(json.dumps(data, indent=2))

# getAddressBookByTitle
#
# (data, retcode, message) = DbInterface.getAddressBookByTitle(1, "Clients")
# if message:
#   print(f"retcode ok = {retcode}, message = {message}")
# else:
#   print(f"retcode ok = {retcode}")
# print(json.dumps(data, indent=2))

# createAddressBook
#
# (retcode, message) = dbInterface.createAddressBook(1, "Friends")
# if message:
#   print(f"retcode ok = {retcode}, message = {message}")
# else:
#   print(f"retcode ok = {retcode}")

# updateAddressBook
#
# (retcode, message) = dbInterface.updateAddressBook(1, "Suppliers")
# if message:
#   print(f"retcode ok = {retcode}, message = {message}")
# else:
#   print(f"retcode ok = {retcode}")

# deleteAddressBook
#
# (retcode, message) = dbInterface.deleteAddressBook(2)
# if message:
#   print(f"retcode ok = {retcode}, message = {message}")
# else:
#   print(f"retcode ok = {retcode}")

# addContactToAddressBook
#
# (retcode, message) = dbInterface.addContactToAddressBook(currentUserId=1, addressBookId=2, contactId=1)
# if message:
#   print(f"retcode ok = {retcode}, message = {message}")
# else:
#   print(f"retcode ok = {retcode}")

# removeContactFromAddressBook
#
# (retcode, message) = dbInterface.removeContactFromAddressBook(1, 1)
# if message:
#   print(f"retcode ok = {retcode}, message = {message}")
# else:
#   print(f"retcode ok = {retcode}")

# getContactsInAllAddressBooks
#
# (data, retcode, message) = dbInterface.getContactsInAllAddressBooks(1)
# if message:
#   print(f"retcode ok = {retcode}, message = {message}")
# else:
#   print(f"retcode ok = {retcode}")
# print(json.dumps(data, indent=2))
