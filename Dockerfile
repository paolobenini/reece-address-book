FROM python:3.8

ENV SQLITE_DB=address_book.db
ENV SECRET_KEY=cblau4rh848hq0vkas4q34isa044i2hs

WORKDIR /reece-address-book-api

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY ./reece_address_book ./reece_address_book

WORKDIR /reece-address-book-api/reece_address_book

CMD ["waitress-serve", "--port=8000", "--host=0.0.0.0", "--call", "app:create_app"]
