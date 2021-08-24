## REECE_ADDRESS_BOOK: Address Book API for Reece

An API to manage address books.

Installation
------------

Pull the latest image from DockerHub (v1.1):

    docker pull paolobenini/reece-address-book-api:v1.1

Deploy on AWS ECS or Kubernetes platform.


API endpoints
-------------

/
- GET: returns a JSON object with the API version.

/login 
- POST: body = JSON object with "email" and "password".

/register
- POST: adds a new user; body = JSON object with "email" and "password".
Returns the auth token.

/users
- GET: returns a JSON object with all users. With optional parameter "user_id", it returns a JSON object containing the requested user.

/contacts
- All methods require the authentication token in http request's header "x-access-tokens".
- GET: returns a JSON object with all unique contacts across all address books for the current user. With optional parameter "contact_id", it returns a JSON object containing the requested contact. With optional parameter "globally=true" returns all contacts for the current user regardless.
- POST: adds a new contact; body = JSON object with "name", "surname", "phone".
- PUT: updates contact with id "contact_id"; body = JSON object containing at least one of the following:
"name", "surname", "phone".
- DELETE: delete contact with id "contact_id".

/address_books
- All methods require the authentication token in http request's header "x-access-tokens".
- Additional parameters: "address_book_id", "title".
- GET: returns a JSON object with all address books, for the current user. With the optional parameter "address_book_id", it returns a JSON object with the requested address book.
- POST: adds a new address book; parameter "title".
- PUT: updates address_book with id "address_book_id".
- DELETE: deletes address_book with id "address_book_id".

/address_book/contacts
- All methods require the authentication token in http request's header "x-access-tokens".
- Additional parameters: "address_book_id" and "contact_id".
- GET: returns a JSON object with all contacts in address book "address_book_id".
- POST: adds contact "contact_id" to address book "address_book_id".
- DELETE: remove contact "contact_id" from address book "address_book_id".
  
Usage
-----

```plain
    # Register user
    /register
    http method: POST
    http request body:
    {
        "email": "john@gmail.com"
        "pasword": "1234"
    }
```

```plain
    # Login user
    /login
    http method: POST
    http request body:
    {
        "email": "john@gmail.com"
        "pasword": "1234"
    }
```

```plain
    # Create a new contact
    /contacts
    http method: POST
    http header "x-access-tokens": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VySWQiOjEsImVtYWlsIjoicGFvbG9AZmFrZWRvbWFpbi5jb20ifQ.jsKRH8-LWMnxSF4Y-PBNPIsbSj_BO-hZV9RZZJas7Th"
    http request body:
    {
        "name": "Paul"
        "surname": "Newman"
        "phone": "0410786990"
    }
```

```plain
    # Update contact first name
    /contacts?contact_id=1
    http method: PUT
    http header "x-access-tokens": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VySWQiOjEsImVtYWlsIjoicGFvbG9AZmFrZWRvbWFpbi5jb20ifQ.jsKRH8-LWMnxSF4Y-PBNPIsbSj_BO-hZV9RZZJas7Th"
    http request body:
    {
        "name": "John"
    }
```

```plain
    # Update contact surname
    /contacts?contact_id=1
    http method: PUT
    http header "x-access-tokens": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VySWQiOjEsImVtYWlsIjoicGFvbG9AZmFrZWRvbWFpbi5jb20ifQ.jsKRH8-LWMnxSF4Y-PBNPIsbSj_BO-hZV9RZZJas7Th"
    http request body:
    {
        "surname": "Charter"
    }
```

```plain
    # Update contact surname and phone
    /contacts?contact_id=1
    http method: PUT
    http header "x-access-tokens": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VySWQiOjEsImVtYWlsIjoicGFvbG9AZmFrZWRvbWFpbi5jb20ifQ.jsKRH8-LWMnxSF4Y-PBNPIsbSj_BO-hZV9RZZJas7Th"
    http request body:
    {
        "surname": "Charter"
        "phone": "0420777888"
    }
```

```plain
    # List all unique contacts across all address books
    /contacts
    http method: GET
    http header "x-access-tokens": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VySWQiOjEsImVtYWlsIjoicGFvbG9AZmFrZWRvbWFpbi5jb20ifQ.jsKRH8-LWMnxSF4Y-PBNPIsbSj_BO-hZV9RZZJas7Th"
```

```plain
    # List all contacts regardless (including contacts which haven't been added to any address book yet)
    /contacts?globally=true
    http method: GET
    http header "x-access-tokens": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VySWQiOjEsImVtYWlsIjoicGFvbG9AZmFrZWRvbWFpbi5jb20ifQ.jsKRH8-LWMnxSF4Y-PBNPIsbSj_BO-hZV9RZZJas7Th"
```

```plain
    # Create a new address book
    /address_books?title=Clients
    http method: POST
    http header "x-access-tokens": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VySWQiOjEsImVtYWlsIjoicGFvbG9AZmFrZWRvbWFpbi5jb20ifQ.jsKRH8-LWMnxSF4Y-PBNPIsbSj_BO-hZV9RZZJas7Th"
```

```plain
    # Add a contact to an address book
    /address_book/contacts?address_book_id=1&contact_id=10
    http method: POST
    http header "x-access-tokens": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VySWQiOjEsImVtYWlsIjoicGFvbG9AZmFrZWRvbWFpbi5jb20ifQ.jsKRH8-LWMnxSF4Y-PBNPIsbSj_BO-hZV9RZZJas7Th"
```

```plain
    # Remove a contact from an address book
    /address_book/contacts?address_book_id=1&contact_id=10
    http method: DELETE
    http header "x-access-tokens": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VySWQiOjEsImVtYWlsIjoicGFvbG9AZmFrZWRvbWFpbi5jb20ifQ.jsKRH8-LWMnxSF4Y-PBNPIsbSj_BO-hZV9RZZJas7Th"
```

```plain
    # List all contacts in address book
    /address_book/contacts
    http method: GET
    http header "x-access-tokens": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VySWQiOjEsImVtYWlsIjoicGFvbG9AZmFrZWRvbWFpbi5jb20ifQ.jsKRH8-LWMnxSF4Y-PBNPIsbSj_BO-hZV9RZZJas7Th"
```

```plain
    # Delete an address book
    /address_books?address_book_id=1
    http method: DELETE
    http header "x-access-tokens": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VySWQiOjEsImVtYWlsIjoicGFvbG9AZmFrZWRvbWFpbi5jb20ifQ.jsKRH8-LWMnxSF4Y-PBNPIsbSj_BO-hZV9RZZJas7Th"
```
