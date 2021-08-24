## REECE_ADDRESS_BOOK: Tests for Address Book API

UNIT TESTS and INTEGRATION TESTS.

Unit Tests
------------

db_interface.py
---------------

Methods:
- DbInterface.getUser: tested OK with valid and invalid parameters
- DbInterface.getUsers: tested OK
- DbInterface.getUserByEmail (currently non used): tested OK with valid and invalid parameters
- DbInterface.getContacts: tested OK
- DbInterface.getContactsInAllAddressBooks: tested OK
- DbInterface.getContactsByFullName (currently non used): tested OK with valid and invalid parameters
- DbInterface.getContactsByFirstName (currently non used): tested OK with valid and invalid parameters
- DbInterface.getContactsBySurname (currently non used): tested OK with valid and invalid parameters
- DbInterface.getContactsByPhone (currently non used): tested OK with valid and invalid parameters
- DbInterface.getContactsByAddressBook: tested OK with valid and invalid parameters
- DbInterface.updateContact: tested OK with valid and invalid parameters
- DbInterface.deleteContact: tested OK with valid and invalid parameters
- DbInterface.createContact: tested OK with valid and invalid parameters
- DbInterface.getAddressBooks: tested OK
- DbInterface.getAddressBookByTitle (currently non used): tested OK with valid and invalid parameters
- DbInterface.createAddressBook: tested OK with valid and invalid parameters
- DbInterface.updateAddressBook: tested OK with valid and invalid parameters
- DbInterface.deleteAddressBook: tested OK with valid and invalid parameters
- DbInterface.addContactToAddressBook: tested OK with valid and invalid parameters
- DbInterface.removeContactFromAddressBook: tested OK with valid and invalid parameters

```plain
    # To test single methods, uncomment relevant block in tests.py and run
    python tests.py
```

Integration Tests
-----------------

Endpoints tested:
- /: root
- /login: login user
- /register: register a new user
- /contacts: get all contacts, get contact by id, add a new contact and delete contact by id
- /address_books: get all address books, get address book by id, add a new address book and delete address book by id
- /address_book/contacts: get all contacts in address book, add contact to address book, remove contact from address book

All endpoints tested both with valid and with invalid arguments.
Run app locally and tested with Postman.
