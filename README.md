# Full-Stack Django Web Project
## Nicoleta Sarghi, Matteo Robidoux, Mohammad Khan
### Group 3, 16 May 2022
### URL: https://dw-42022-prj-grp3-sarghi.herokuapp.com/
### REPO: https://gitlab.com/nicsarghi/project2-python/

## How to run
### Project initialization
1. Create a virtual environment for the project by running
    ```commandline
    python -m venv ./venv
    ```
2. Active the virtual environment
    
    Windows cmd:
    ```commandline
    venv\Scripts\activate.bat
    ```
   
    Linux:
    ```commandline
    source .venv/bin/activate  
    ```

   (See other activation methods [here](https://docs.python.org/3/library/venv.html))

3. Install requirements.txt packages through pip
    ```commandline
    pip install -r requirements.txt
   ```
   
### Database initialization
4. Set up postgresql on your machine
5. Connect to your postgres server and create a user with the following credentials
    ```commandline
    USER: project_admin
    PASSWORD: Python_420
    ```
6. While creating the user, give them access to the database called ``catalog_project``. They must own the database.
7. Run migrations
    ```commandline
    python catalog_project/manage.py migrate
    ```
8. Initialize the dataset (users, groups, posts, etc.) for the site:
    ```commandline
    python catalog_project/manage.py initadmins
    ```

### Running the server
9. You can now run the website using manage.py!
    ```commandline
    python catalog_project/manage.py runserver
   ```

## Website details
The website is used to upload and showcase academic projects of many types from various academic fields.
### Members, Users and Registration
Non-registered users (visitors) can view the overview of projects such as title, author, field, status, etc. and trying to view details of such projects will lead them to the login page as only registered members can view project details or they can register to be a member. Visitors can also directly login using the button in the header if they have an account.

Registered members have a profile whose details can be edited, such as username and profile picture that is displayed publicly, and the password can be reset using the old password. Registered members can view project details such as content and access to the URL linking to the academic paper as well as being able to add comments to a post, like posts, and rate posts based on a scale of 5 (represented by stars). Members can access other members' profiles by clicking on a post author's name.

### Messaging and notifications
Members can send messages to each other and receive notifications, which are shown on the top right of the website with a counter for unread notifications that can be clicked to open all notifications and mark them as read. Notifications are also sent for administrator warnings to users.

### Item catalog and posting
Posts on the website can be rearranged to be view in 2 different layouts, either grid format or list format, and each contain a picture for the academic paper, a post author, the type of paper, the field of study, the paper's status, and keywords. When accessed by a registered user, a post's content is revealed and the link to access the paper is made available.

Anyone can search for posts by selecting a filter and pressing the search button. Not specifying anything in the search bar will reset the search query.

### API
Any logged in user can view the items by going [here](https://dw-42022-prj-grp3-sarghi.herokuapp.com/api/items/) .
This page will list all of the items on the website. The user can also choose filter settings for the query.

Other API features:
- Viewing a specific item: [api/items/<item_id>](https://dw-42022-prj-grp3-sarghi.herokuapp.com/api/items/1/) 
- Editing and deleting an item: [/api/items/manage/<item_id>](https://dw-42022-prj-grp3-sarghi.herokuapp.com/api/items/manage/1/)  (Note that only item admins, superusers or the person who owns the item can view this.)
- Creating an item: [/api/items/create/](https://dw-42022-prj-grp3-sarghi.herokuapp.com/api/items/create/)

### Administration
#### Superuser:
The superuser menu can be accessed through https://dw-42022-prj-grp3-sarghi.herokuapp.com/django-admin which allows superuser privileges after logging in. 
 Superusers who are logged in to the website have all privileges described for the other two categories of administrators.

Known permissions:
- View the superuser dashboard (https://dw-42022-prj-grp3-sarghi.herokuapp.com/admin/)
- View the member admin dashboard (https://dw-42022-prj-grp3-sarghi.herokuapp.com/useradmin/)
- Block a user
- View logs
- Create a user in any group
- Edit a user and set their group
- Flag a user
- Warn a user
- Delete a user
- Edit posts
- Delete posts
- Flag posts

#### Item Admin:
Item administrators have the ability to edit and flag posts for reviewing, and user administrators have the ability to warn, flag, delete and block users from logging in as well as create new users from the user admin dashboard.
Known permissions:
- Edit posts
- Delete posts
- Flag posts

#### Member Admin:
Known permissions:
- View the member admin dashboard (https://dw-42022-prj-grp3-sarghi.herokuapp.com/useradmin/)
- Block a user
- Create a user
- Flag a user
- Warn a user
- Delete a user

#### Dev:
Dev is a superuser that has access to the django-admin dashboard (https://dw-42022-prj-grp3-sarghi.herokuapp.com/django-admin/).
Intended to represent the developer who may or may not need to modify superusers and whatnot.




