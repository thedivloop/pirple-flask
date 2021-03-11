# Full stack developper - Homework 3

## Scaffolding
Given the specs above, make a list of all the individual routes and pages that will need to exist on your application. Now actually create those routes, and the empty HTML templates. 

## Routes
- Homepage
- Terms of use
- Privacy
- About us

## Login
A visitor should be able to signup (with email and password). If the email address already exists then the signup should fail. On subsequent visits, the user should be able to login and logout with those credentials.

## Dashboard access
Once a user is created (or when they login) they should be taken to their dashboard. Their dashboard should display any "Todo Lists" they've created so far.

## List Management (CRUD)
From the dashboard they should be able to create a new list or click on any existing list.

## Tasks Management (CRUD)
Once a list is created or visited, the user should be able to view all of the tasks on that list. The user should be able to name/rename the list, add tasks, remove tasks, or "check off" tasks as complete. They should also be able to delete the entire list.

## Assignment

### Create Routes
Given the specs above, make a list of all the individual routes and pages that will need to exist on your application. Now actually create those routes, and the empty HTML templates. Don't worry about filling in functionality yet, you are just creating the scaffolding of the application.

**Routes and HTML files**

- structure.html

*Public*

- /home : homepage.html
- /index : index.html
- /about : about.html
- /terms : terms.html
- /privacy : privacy.html
- /signup : signup.html
- /login : route only (->index.html)
- /getsession : route only
- /logout : route only

*Private*

- /dashboard : dashboard.html


### Select DB
Choose the database you'd like to use for your app (MySQL, PostgreSQL, etc). Whatever the choice, you'll want to install a working version of the database within your Ubuntu VM so your application can connect to it.

- Database selection : sqlite3
- Installation : completed

### DB Schema
Design the database schema for your application. How many tables should exist? What columns should exist within those tables, and what should their data-types be? Once you've thought it out, now's the time to actually create those tables within the DB. Once you're done, export your schema / table-structure and that file in your application's folder. Don't worry about the data models yet, we'll tackle that in the next homework.

#### Tables

**Users**

| Field | UserID | Username | first name | last name | password |
| ----------- | ----------- | ----------- | ----------- | ----------- | ----------- |
| data type | *INTEGER: autoincrement* | *VARCHAR(16)* | *VARCHAR(16)* | *VARCHAR(16)* | *VARCHAR(32)* |
| Example | *789* | *babyman* | *Pierre* | *Jacques* | ********** |

**Lists**

| Field | List ID | UserID | list name | number of tasks |
| ----------- | ----------- | ----------- | ----------- | :-----------: |
| data type | *INTEGER: autoincrement* | *INTEGER* | *VARCHAR(32)* | *INTEGER* |
| Example | *3* | *789* | *Do Groceries* | *5* |

**Tasks**

| Field | TaskID | List ID | Task name | 
| ----------- | ----------- | ----------- | :-----------: |
| data type | *INTEGER: autoincrement* | *INTEGER* | *VARCHAR(32)* |
| Example | *7* | *3* | *Buy milk* |

