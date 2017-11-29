# Item Catalog Application

## Introduction
The purpose of this project is to develop an application that provides a list
of items within a variety of categories as well as provide a user registration
and authentication system.  Registered users will have the ability to post,
edit, and delete their own items.  I had to combine my knowledge of building
dynamic website with persistent data storage to create a web application that
provides a compelling service to my users.

---

## Getting Started

### Required downloads
1. Clone or download this repository.
2. Download [Vagrant](https://vagrantup.com/ "Vagrant link")
3. Download [VirtualBox](https://www.virtualbox.org/ "Virtualbox link")

### Required actions
1. Open directory in terminal and use these commands:
2. vagrant up
3. vagrant ssh
4. cd /vagrant
5. cd catalog
6. python application.py
7. In your web browser, open "http://localhost:5000"

---

### Files included
#### static (folder)
This folder contains the CSS code to format the style of the app, as well as
the picture used for the background image.

#### templates (folder)
This folder contains all HTML templates.

#### application.py
This is Python code used to run the app.

#### client_secrets.JSON
JSON script necessary to interact with the Google API.

#### database_setup.py
Python code that creates the database and tables.

#### lotsofmenus.py
Python code that populates the database with several restaurants and menu items.

#### restaurantmenu.db
Database file.