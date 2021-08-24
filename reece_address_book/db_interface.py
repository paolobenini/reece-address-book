""" This module contain the Query class. """
import datetime
from sqlalchemy import and_, or_, func
from models import *

class DbInterface:
  """
  This class provide methods to perform query on the database, create, update and delete records.
  Data is returned as a retcode, as a dictionary or as a list of dictionaries.
  """
  def __init__(self, db_instance):
    self.__db = db_instance

  @staticmethod
  def getUser(userId: int):
    retcodeOk = True
    message = ""
    userData = {}
    if userId > 0:
      user = User.query.get(userId)
      if user != None:
        userData["id"] = user.id
        userData["email"] = user.email
      else:
        retcodeOk = False
        message = "Error: no user found."
    else:
      retcodeOk = False
      message = "Error: userId must be a positive integer."
    return (userData, retcodeOk, message)

  @staticmethod
  def getUsers():
    """
    Get users. 
    
    Returns: 
      (output, retcodeOk, message)
    """    
    retcodeOk = True
    message = ""
    output = []
    users = User.query.all()
    if users:
      for user in users:
        result = User.query.get(user.id)
        if result != None:
          userData = {}
          userData["id"] = user.id
          userData["email"] = user.email
          output.append(userData)
        else:
          retcodeOk = False
          message = "Error: no user found."
      return (output, retcodeOk, message)
    else:
      retcodeOk = False
      message = "Error: no user found."
      return (output, retcodeOk, message)

  @staticmethod
  def getUserByEmail(email: str):
    """
    Get user by email. 
    
    Parameters: 
      email
        
    Returns: 
      (userData, retcodeOk, message)
    """
    retcodeOk = True
    message = ""
    userData = {}
    user = User.query.filter(User.email == email).first()
    if user != None:
      userData["id"] = user.id
      userData["email"] = user.email
    else:
      retcodeOk = False
      message = "Error: no user found."
    return (userData, retcodeOk, message)

  @staticmethod
  def getContacts(userId: int):
    """ 
    Get all contacts for any given user regardless of their belonging to any address book.
    
    Parameters: 
      userId
        
    Returns: 
      (output, retcodeOk, message)
    """
    retcodeOk = True
    message = ""
    output = []
    if userId > 0:
      contacts = Contact.query.filter(Contact.userId == userId).all()
      if contacts:
        for contact in contacts:
          contactData = {}
          contactData["id"] = contact.id
          contactData["name"] = contact.name
          contactData["surname"] = contact.surname
          contactData["phone"] = contact.phoneNumber
          output.append(contactData)
      else:
        retcodeOk = False
        message = "Error: no records found."
    else:
      retcodeOk = False
      message = "Error: userId must be a positive integer."
    return (output, retcodeOk, message)

  @staticmethod
  def getContactsInAllAddressBooks(userId: int):
    """ 
    Get all contacts for any given user in all address books.
    
    Parameters: 
      userId
        
    Returns: 
      (output, retcodeOk, message)
    """
    retcodeOk = True
    message = ""
    output = []
    if userId > 0:
      contacts = Contact.query.join(ContactAddressBook, Contact.id == ContactAddressBook.contactId). \
                filter(Contact.userId == userId).all()
      # debug
      #      
      print(contacts)
      if contacts:
        for contact in contacts:
          contactData = {}
          contactData["id"] = contact.id
          contactData["name"] = contact.name
          contactData["surname"] = contact.surname
          contactData["phone"] = contact.phoneNumber
          output.append(contactData)
      else:
        retcodeOk = False
        message = "Error: no records found."
    else:
      retcodeOk = False
      message = "Error: userId must be a positive integer."
    return (output, retcodeOk, message)

  @staticmethod
  def getContact(contactId: int):
    """ 
    Get a contact by id. 

    Parameters: 
      contactId
        
    Returns: 
      (contactData, retcodeOk, message)
    """
    retcodeOk = True
    message = ""
    contactData = {}
    if contactId > 0:
      contact = Contact.query.get(contactId)
      if contact != None:
        contactData["id"] = contact.id
        contactData["name"] = contact.name
        contactData["surname"] = contact.surname
        contactData["phone"] = contact.phoneNumber
      else:
        retcodeOk = False
        message = "Error: no records found."
    else:
      retcodeOk = False
      message = "Error: contactId must be a positive integer."
    return (contactData, retcodeOk, message)

  def updateContact(self, contactId: int, name: str, surname: str, phoneNumber: str):
    """ 
    Update a contact. 

    Parameters: 
      contactId, name, surname, phoneNumber
        
    Returns: 
      (retcodeOk, message)
    """
    retcodeOk = True
    message = "Contact updated successfully"
    if contactId > 0:
      contact = Contact.query.get(contactId)
      if contact != None:
        try:
          contact.name = name
          contact.surname = surname
          contact.phoneNumber = phoneNumber
          self.__db.session.commit()
        except:
          message = "Error: database error."
          retcodeOk = False
      else:
        message = "Error: no contact with that id."
        retcodeOk = False
    else:
      retcodeOk = False
      message = "Error: contactId must be a positive integer."
    return (retcodeOk, message)

  def deleteContact(self, contactId: int):
    """ 
    Delete a contact.

    Parameters: 
      contactId
        
    Returns: 
      (retcodeOk, message)
    """
    retcodeOk = True
    message = "Contact deleted successfully"
    if contactId > 0:
      contacts = Contact.query.filter_by(id = contactId)
      if contacts.first() != None:
        try:
          contacts.delete()
          self.__db.session.commit()
        except:
          message = "Error: database error."
          retcodeOk = False
      else:
        message = "Error: no contact with that id."
        retcodeOk = False
    else:
      retcodeOk = False
      message = "Error: contactId must be a positive integer."
    return (retcodeOk, message)

  def createContact(self, userId: int, name: str, surname: str, phoneNumber: str):
    """ 
    Create a new contact. Contacts are private to each user.
    Check if the phoneNumber already exixts and do not create a new
    contact if it does.

    Parameters: 
      userId, name, surname, phoneNumber
        
    Returns: 
      (retcodeOk, message)
    """
    retcodeOk = True
    message = "Contact created successfully"
    if userId > 0:
      # Clean inputs
      nameTrimmed = name.strip()
      surnameTrimmed = surname.strip()
      phoneNumberTrimmed = phoneNumber.strip()
      result = Contact.query.filter(Contact.phoneNumber == phoneNumberTrimmed).first()
      if result == None:
        contact = Contact(userId=userId, name=nameTrimmed, surname=surnameTrimmed, phoneNumber=phoneNumberTrimmed, \
                  dateCreated=datetime.datetime.utcnow())
        try:
          self.__db.session.add(contact)
          self.__db.session.commit()
        except:
          message = "Error: database error."
          retcodeOk = False
      else:
          message = "Error: this phone number already exists."
          retcodeOk = False
    else:
      retcodeOk = False
      message = "Error: userId must be a positive integer."
    return (retcodeOk, message)

  @staticmethod
  def getContactsByFullName(name: str, surname: str):
    """ 
    Get all contacts with a given full name. Name and surname are converted to lower case for 
    the purpose of this search.

    Parameters: 
      name, surname

    Returns: 
      (output, retcodeOk, message)
    """
    # Clean inputs
    nameTrimmed = name.strip()
    surnameTrimmed = surname.strip()
    contacts = Contact.query.filter(and_(func.lower(Contact.name) == func.lower(nameTrimmed), \
                                    func.lower(Contact.surname) == func.lower(surnameTrimmed))).all()
    output = []
    retcodeOk = True
    message = ""
    if contacts:
      for contact in contacts:
        contactData = {}
        contactData["id"] = contact.id
        contactData["name"] = contact.name
        contactData["surname"] = contact.surname
        contactData["phone number"] = contact.phoneNumber
        output.append(contactData)
    else:
      retcodeOk = False
      message = "Error: no contacts found."
    return (output, retcodeOk, message)

  @staticmethod
  def getContactsByFirstName(name: str):
    """ 
    Get all contacts with a given first name. Name is converted to lower case for 
    the purpose of this search.

    Parameters: 
      name

    Returns: 
      (output, retcodeOk, message)
    """
    # Clean inputs
    nameTrimmed = name.strip()
    contacts = Contact.query.filter(func.lower(Contact.name) == func.lower(nameTrimmed)).all()
    output = []
    retcodeOk = True
    message = ""
    if contacts:
      for contact in contacts:
        contactData = {}
        contactData["id"] = contact.id
        contactData["name"] = contact.name
        contactData["surname"] = contact.surname
        contactData["phone number"] = contact.phoneNumber
        output.append(contactData)
    else:
      retcodeOk = False
      message = "Error: no contacts found."
    return (output, retcodeOk, message)
  
  @staticmethod
  def getContactsBySurname(surname: str):
    """ 
    Get all contacts with a given surname. Surame is converted to lower case for 
    the purpose of this search.

    Parameters: 
      surnmame

    Returns: 
      (output, retcodeOk, message)
    """
    # Clean inputs
    surnameTrimmed = surname.strip()
    contacts = Contact.query.filter(func.lower(Contact.surname) == func.lower(surnameTrimmed)).all()
    output = []
    retcodeOk = True
    message = ""
    if contacts:
      for contact in contacts:
        contactData = {}
        contactData["id"] = contact.id
        contactData["name"] = contact.name
        contactData["surname"] = contact.surname
        contactData["phone number"] = contact.phoneNumber
        output.append(contactData)
    else:
      retcodeOk = False
      message = "Error: no contacts found."
    return (output, retcodeOk, message)

  @staticmethod
  def getContactsByPhone(phoneNumber: str):
    """ 
    Get all contacts with a given phone number. 

    Parameters: 
      phoneNumber

    Returns: 
      (output, retcodeOk, message)
    """
    # Clean inputs
    phoneNumberTrimmed = phoneNumber.strip()
    contacts = Contact.query.filter(Contact.phoneNumber == phoneNumberTrimmed).all()
    output = []
    retcodeOk = True
    message = ""
    if contacts != None:
      for contact in contacts:
        contactData = {}
        contactData["id"] = contact.id
        contactData["name"] = contact.name
        contactData["surname"] = contact.surname
        contactData["phone number"] = contact.phoneNumber
        output.append(contactData)
    else:
      retcodeOk = False
      message = "Error: no contacts found."
    return (output, retcodeOk, message)

  @staticmethod
  def getContactsByAddressBook(addressBookId: int):
    """ 
    Get all contacts in a given address book. 
        
    Parameters: 
      addressBookId

    Returns: 
      (output, retcodeOk, message)
    """
    retcodeOk = True
    message = ""
    output = []
    if addressBookId > 0:
      records = ContactAddressBook.query.filter(ContactAddressBook.addressBookId == addressBookId).all()
      if records:
        contactIds = [record.contactId for record in records]
        contacts = Contact.query.filter(Contact.id.in_(contactIds)).all()
        if contacts:
          for contact in contacts:
            contactData = {}
            contactData["id"] = contact.id
            contactData["name"] = contact.name
            contactData["surname"] = contact.surname
            contactData["phone number"] = contact.phoneNumber
            output.append(contactData)
        else:
          retcodeOk = False
          message = "Error: no contacts found."
      else:
        retcodeOk = False
        message = "Error: no contacts found."
    else:
      retcodeOk = False
      message = "Error: addressBookId must be a positive integer."
    return (output, retcodeOk, message)

  @staticmethod
  def getAddressBooks(userId: int):
    """ 
    Get address books by userId. 

    Parameters: 
      userId

    Returns: 
      (output, retcodeOk, message)
    """
    retcodeOk = True
    message = ""
    output = []
    if userId > 0:
      addressBooks = AddressBook.query.filter(AddressBook.userId == userId).all()
      if addressBooks:
        for addressBook in addressBooks:
          addressBookData = {}
          addressBookData["id"] = addressBook.id
          addressBookData["title"] = addressBook.title
          output.append(addressBookData)
      else:
        retcodeOk = False
        message = "Error: no record found."
    else:
      retcodeOk = False
      message = "Error: userId must be a positive integer."
    return (output, retcodeOk, message)

  @staticmethod
  def getAddressBook(addressBookId: int):
    """ 
    Get address book by id. 

    Parameters: 
      addressBookId

    Returns: 
      (output, retcodeOk, message)
    """
    retcodeOk = True
    message = ""
    addressBookData = {}
    if addressBookId > 0:
      addressBook = AddressBook.query.get(addressBookId)
      if addressBook != None:
        addressBookData["id"] = addressBook.id
        addressBookData["title"] = addressBook.title
      else:
        retcodeOk = False
        message = "Error: no record found."
    else:
      retcodeOk = False
      message = "Error: addressBookId must be a positive integer."
    return (addressBookData, retcodeOk, message)

  @staticmethod
  def getAddressBookByTitle(userId: int, title: str):
    """ 
    Get address book by title. Title is converted to lower case for the
    purpose of this search.

    Parameters: 
      userId, title

    Returns: 
      (addressBookData, retcodeOk, message)
    """
    # Clean inputs
    titleTrimmed = title.strip()
    retcodeOk = True
    message = ""
    addressBookData = {}
    if userId > 0:
      user = User.query.get(userId)
      if user:
        addressBook = AddressBook.query.filter(and_(func.lower(AddressBook.title) == func.lower(titleTrimmed), \
                      AddressBook.userId == userId)).first()
        if addressBook != None:
          addressBookData["id"] = addressBook.id
          addressBookData["title"] = addressBook.title
        else:
          retcodeOk = False
          message = "Error: no record found."
      else:
        retcodeOk = False
        message = "Error: no user with that id."
    else:
      retcodeOk = False
      message = "Error: userId must be a positive integer."

    return (addressBookData, retcodeOk, message)

  def createAddressBook(self, userId: int, title: str):
    """ 
    Create a new empty address book only if the title doesn't already exist. 
    
    Parameters: 
      userId, title

    Returns: 
      (retcodeOk, message) 
    """
    retcodeOk = True
    message = "Address book created successfully."
    if userId > 0:
      # Clean inputs
      titleTrimmed = title.strip()
      result = AddressBook.query.filter(func.lower(AddressBook.title) == func.lower(titleTrimmed)).first()
      if result == None:
        addressBook = AddressBook(userId=userId, title=titleTrimmed, dateCreated=datetime.datetime.utcnow())
        try:
          self.__db.session.add(addressBook)
          self.__db.session.commit()
        except:
          message = "Error: database error."
          retcodeOk = False
      else:
        message = "Error: an address book with that name already exists."
        retcodeOk = False
    else:
      retcodeOk = False
      message = "Error: userId must be a positive integer."
    return (retcodeOk, message)

  def updateAddressBook(self, addressBookId: int, title: str):
    """ 
    Update an address book. 
    
    Parameters: 
      addressBookId, title

    Returns: 
      (retcodeOk, message)
    """
    retcodeOk = True
    message = "Address book updated successfully."
    if addressBookId > 0:
      # Clean inputs
      titleTrimmed = title.strip()
      addressBook = AddressBook.query.get(addressBookId)
      if addressBook != None:
        try:
          addressBook.title = titleTrimmed
          self.__db.session.commit()
        except:
          message = "Error: database error."
          retcodeOk = False
      else:
        message = "Error: no record found."
        retcodeOk = False
    else:
      retcodeOk = False
      message = "Error: addressBookId must be a positive integer."
    return (retcodeOk, message)

  def deleteAddressBook(self, addressBookId: int):
    """ 
    Delete an address book. Contacts are not deleted, only the address book. 
    
    Parameters: 
      addressBookId

    Returns: 
      (retcodeOk, message)
    """
    retcodeOk = True
    message = "Address book deleted successfully."
    if addressBookId > 0:
      addressBooks = AddressBook.query.filter_by(id = addressBookId)
      if addressBooks.first() != None:
        records = ContactAddressBook.query.filter(ContactAddressBook.addressBookId == addressBookId)
        if records.first() != None:
          try:
            records.delete()
            self.__db.session.commit()
          except:
            message = "Error: database error."
            retcodeOk = False
        try:
          addressBooks.delete()
          self.__db.session.commit()
        except:
          message = "Error: database error."
          retcodeOk = False
      else:
        message = "Error: no record found."
        retcodeOk = False
    else:
      retcodeOk = False
      message = "Error: addressBookId must be a positive integer."
    return (retcodeOk, message)
  
  def addContactToAddressBook(self, currentUserId: int, addressBookId: int, contactId: int):
    """ 
    The given contact is added to an address book only if the current address book belongs to the user. 
    
    Parameters: 
      currentUserId, addressBookId, contactId

    Return: 
      (retcodeOk, message)
    """
    retcodeOk = True
    message = "Contact added successfully"
    if currentUserId > 0 and addressBookId > 0:
      contact = Contact.query.get(contactId)
      addressBook = AddressBook.query.get(addressBookId)
      if contact != None and \
        addressBook != None and \
        contact.userId == currentUserId:
        contactInAddressBook = ContactAddressBook.query.filter(and_(contactId == ContactAddressBook.contactId, \
                              addressBookId == ContactAddressBook.addressBookId)).first()
        if not contactInAddressBook:
          record = ContactAddressBook(addressBookId=addressBookId, contactId=contactId)
          try:
            self.__db.session.add(record)
            self.__db.session.commit()
          except:
            retcodeOk = False
            message = "Error: database error."
        else:
          retcodeOk = False
          message = "Error: the contact is already in this address book."
      else:
        retcodeOk = False
        message = "Error: either the address book or the contact doesn't exist."
    else:
      retcodeOk = False
      message = "Error: ids must be positive integers."
    return (retcodeOk, message)

  def removeContactFromAddressBook(self, addressBookId: int, contactId: int):
    """ 
    Remove a contact from an address book.

    Parameters: 
      addressBookId, contactId

    Return: 
      (retcodeOk, message)
    """
    retcodeOk = True
    message = "Contact has been removed from address book."
    if addressBookId > 0 and contactId > 0:
      records = ContactAddressBook.query.filter(ContactAddressBook.contactId == contactId)
      if records.first() != None:
        try:
          records.delete()
          self.__db.session.commit()
        except:
          retcodeOk = False
          message = "Error: database error."
      else:
        retcodeOk = False
        message = "Error: no record found."
    else:
      retcodeOk = False
      message = "Error: ids must be positive integers."
    return (retcodeOk, message)

