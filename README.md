# Project 4 - Item Catalog

# Introduction

The porpose of this project is to implement a webpage with Flask and CRUD functionalities
with sqlalchemy to maintain a database.
It provides user authentication with Google account, user registration system and
JSON API for all items and categories. All the users can see the categories and items but
only registered users can modify them.

# Setup

Clone this repository.

The repository contains:
- application.py - this file runs the program, implements the crud functionality and
user authentication/registration
- database_setup.py - this file sets up the database structure
- data_creating.py - thi file creates some example data
- items_catalog.db - contains the data
- static - contains the HTML templates and CSS files for the webpage
- client_secrets.json - the dictionary for client id and secrets
(the sensitive information is hidden)
- the Vagrant files
- this README.md file

The database contains the following tables with the following columns:
- category: id(PK), name, user_id(FK)
- user: id(PK), name, email, picture
- item: id(PK), name, description, price, category_id(FK), user_id(FK)

If you do not have the necessary programs, you will need to install the followings:
- Python3
- the Python packages imported in the python files
- Vagrant
- Virtual Box

# Running

Launch Vagrant by running vagrant up from the command line, then log with
vagrant ssh.

- Access the program files though Vagrant.
- Run the database_setup.py to setup the database.
- Run the data_creating.py to populate the database.
- After that, run the application.py  
- Navigate to http://localhost:5000/main to get the main page. I you want to modify
the data, register and log in with your Google account.
