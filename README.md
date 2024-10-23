# Product Management System

## Introduction

The **Laptop Store** is a web application designed to streamline the management of product information for laptopstores. This project provides a user-friendly interface that allows administrators to efficiently add, update, delete, and view product details. Built using **Flask**, a lightweight web framework for Python, the application leverages **SQLAlchemy** for database interactions and **MySQL** for data storage.

### Key Features

- **User Authentication**: Secure login system for administrators to manage products.
- **Product Management**: Add, update, delete, and view product details with ease.
- **Image Upload**: Upload and store images for each product, enhancing product listings and user image.

### Technology Stack

- **Backend**: Python with Flask
- **Database**: MySQL
- **Frontend**: HTML, CSS, and JavaScript

## Prerequisites

- **Python**: This project requires Python 3.6 or higher. You can download it from [python.org](https://www.python.org/downloads/).

- **Flask**: A lightweight web framework for Python.
  - Install using `pip install Flask`.

- **Flask-SQLAlchemy**: An extension for Flask that adds support for SQLAlchemy.
  - Install using `pip install Flask-SQLAlchemy`.

- **Flask-Migrate**: An extension that handles SQLAlchemy database migrations for Flask applications.
  - Install using `pip install Flask-Migrate`.

- **PyMySQL**: A pure-Python MySQL client library.
  - Install using `pip install PyMySQL`.


## Project Checklist
- [x] It is available on GitHub.
- [x] It uses the Flask web framework.
- [x] It uses at least one module from the Python Standard Library other than the random module.
  Please provide the name of the module you are using in your app. 
  - Module name: json, os, secrets.
  [x] It contains at least one class written by you that has both properties and methods. It uses `__init__()` to let the class initialize the object's attributes (note that  `__init__()` doesn't count as a method). This includes instantiating the class and using the methods in your app. Please provide below the file name and the line number(s) of at least one example of a class definition in your code as well as the names of two properties and two methods.
  - File name for the class definition: User
   Line number(s) for the class definition: line 11 in user.
    Name of two properties: name, phone, email,username,password,isAdmin,image,created_at
  - Name of two methods: getUserByEmail, check_credentials.
    - File name and line numbers where the methods are used: routes.py , line 20,36
- [x] It makes use of JavaScript in the front end and uses the localStorage of the web browser.
- [x] It makes use of the reading and writing to the same file feature.
- [x] It contains conditional statements. Please provide below the file name and the line number(s) of at least
  one example of a conditional statement in your code.
  - File name: user.py .
  - Line number(s): 38, 39, 48, 55, ..............
- [x] It contains loops. Please provide below the file name and the line number(s) of at least
  one example of a loop in your code.
  - File name: index.html.
  - Line number(s):77.
- [x] It lets the user enter a value in a text box at some point.
  This value is received and processed by your back end Python code.
- [x] It doesn't generate any error message even if the user enters a wrong input.
- [x] It is styled using CSS.
- [x] The code follows the code and style conventions as introduced in the course, is fully documented using comments and doesn't contain unused or experimental code. 
  In particular, the code should not use `print()` or `console.log()` for any information the app user should see. Instead, all user feedback needs to be visible in the browser.  
- [x] All exercises have been completed as per the requirements and pushed to the respective GitHub repository.
