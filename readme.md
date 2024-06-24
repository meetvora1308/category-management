# Category Management Project

## Overview


This project is designed to manage categories and products with a multi-level hierarchy. It includes functionalities for creating categories up to n levels deep and associating products with multiple categories. Please note that this project does not include user authentication or authorization And It runs on Ubuntu and requires Python 3.10.12 and redis.

## Setup Instructions

1. Clone the project repository or download the zip file.
2. Navigate to the root directory of the project.
3. Create a virtual environment:
   `python3 -m venv venv`
4. Activate the virtual environment:
   `source venv/bin/activate`
5. Install all dependencies listed in requirements.txt:
   `pip install -r requirements.txt`
6. To create users using Django management command:
   `python manage.py create_users`
7. make migrate to make the database changes using command:
  `python manage.py migrate`
8. You can open a new terminal and activate the virtual environment as needed.
9. Start the Django server:
   `python manage.py runserver`
10. In a second terminal, start the Celery worker for asynchronous tasks:
   `celery -A CategoryManagement worker --loglevel=info`

## Endpoints

### Category Endpoint

- **Create a Category:**

  `curl -X POST http://127.0.0.1:8000/categories/ -H "Content-Type: application/json" -d '{"name": "Electronics"}'`

  `curl -X POST http://127.0.0.1:8000/categories/ -H "Content-Type: application/json" -d '{"name": "Computers", "parent": 1}'`

- **Update a Category:**

  `curl -X PUT http://127.0.0.1:8000/categories/<id>/ -H "Content-Type: application/json" -d '{"name": "Electronics"}'`

- **Delete a Category:**

  `curl -X DELETE http://127.0.0.1:8000/categories/<id>/ -H "Content-Type: application/json"`

- **Get all Categories:**

  `curl -X GET http://127.0.0.1:8000/categories/ -H "Content-Type: application/json"`

### Product Endpoint

- **Create a Product:**
  
  `curl -X POST http://127.0.0.1:8000/product/ -H "Content-Type: application/json" -d '{"name": "MacBook Pro", "price": 1999.99, "categories": [2, 3]}'`

  `curl -X POST http://127.0.0.1:8000/product/ -H "Content-Type: application/json" -d '{"name": "iMac", "categories": [1]}'`

- **Update a Product:**

  `curl -X PUT http://127.0.0.1:8000/product/<id>/ -H "Content-Type: application/json" -d '{"name": "MacBook Pro 2023"}'`

- **Delete a Product:**

  `curl -X DELETE http://127.0.0.1:8000/product/<id>/ -H "Content-Type: application/json"`

- **Get all Products:**
  
  `curl -X GET http://127.0.0.1:8000/product/ -H "Content-Type: application/json"`

### Cache Endpoint

- **Retrieve Products from Cache:**

  `curl -X GET http://127.0.0.1:8000/products_cache/ -H "Content-Type: application/json"`


### Email Endpoint

- **Normal Email without 2 min delay:**

  `curl -X POST http://127.0.0.1:8000/emaiuser/ -H "Content-Type: application/json" -d '{"email": "any email"}'`

- **Email with 2 min delay:**

  `curl -X POST http://127.0.0.1:8000/emaiuser/send_mail/ -H "Content-Type: application/json" -d '{"email": "any email"}'`


## Additional Notes

- Replace `<id>` in the endpoint URLs with the actual ID of the category or product you want to interact with.
- Make sure to adjust the base URL (`http://127.0.0.1:8000`) if your development server runs on a different host or port.
