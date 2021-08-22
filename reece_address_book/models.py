""" This module contain the Database model classes. """
from init_app import db

class User(db.Model):
  """ Users: this class allows to have more than one user.
      It could be useful in the future to expand it to other
      staff and/or managers.
  """
  __tablename__ = "users"
  id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
  email = db.Column(db.String(255), unique=True, nullable=False)
  password = db.Column(db.String(255), nullable=False)

class AddressBook(db.Model):
  """ AddressBook: this class describe a generic Address Book.
      Every user can have one or more address books.
  """
  __tablename__ = "address_books"
  id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
  # Foreign Key
  userId = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
  title = db.Column(db.String(255), nullable=False)
  # This can be useful for ordering by date
  dateCreated = db.Column(db.DateTime, nullable=False)

class Contact(db.Model):
  """ Contact: this class describe a generic contact.
      Contacts belong the user who created them.
  """
  __tablename__ = "contacts"
  id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
  # Foreign Key
  userId = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
  name = db.Column(db.String(255), nullable=False)
  surname = db.Column(db.String(255), nullable=False)
  # Phone number should be unique
  phoneNumber = db.Column(db.String(255), nullable=False, unique=True)
  # This can be useful for ordering by date
  dateCreated = db.Column(db.DateTime, nullable=False)

class ContactAddressBook(db.Model):
  """ ContactAddressBook: this class describe a linking table between 'contacts' and 'address_books'.
      It is a way to represent a many to many relationship.
  """
  __tablename__ = "contacts_addressbooks"
  addressBookId = db.Column(db.Integer, db.ForeignKey("address_books.id", ondelete="CASCADE", onupdate="CASCADE"), primary_key=True, nullable=False)
  contactId = db.Column(db.Integer, db.ForeignKey("contacts.id", ondelete="CASCADE", onupdate="CASCADE"), primary_key=True, nullable=False)


