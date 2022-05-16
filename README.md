# Full-Stack Django Web Project
# Nicoleta Sarghi, Matteo Robidoux, Mohammad Khan
# 16 May 2022
# URL: https://dw-42022-prj-grp3-sarghi.herokuapp.com/

The website is used to upload and showcase academic projects of many types from various academic fields.

Non-registered users (visitors) can view the overview of projects such as title, author, field, status, etc. and trying to view details of such projects will lead them to the login page as only registered members can view project details or they can register to be a member. Visitors can also directly login using the button in the header if they have an account.

Registered members have a profile whose details can be edited, such as username and profile picture that is displayed publicly, and the password can be reset using the old password. Registered members can view project details such as content and access to the URL linking to the academic paper as well as being able to add comments to a post, like posts, and rate posts based on a scale of 5 (represented by stars). Members can access other members' profiles by clicking on a post author's name.

Members can send messages to each other and receive notifications, which are shown on the top right of the website with a counter for unread notifications that can be clicked to open all notifications and mark them as read. Notifications are also sent for administrator warnings to users.

Posts on the website can be rearranged to be view in 2 different layouts, either grid format or list format, and each contain a picture for the academic paper, a post author, the type of paper, the field of study, the paper's status, and keywords. When accessed by a registered user, a post's content is revealed and the link to access the paper is made available.

The superuser menu can be accessed through https://dw-42022-prj-grp3-sarghi.herokuapp.com/django-admin which allows superuser privileges after logging in. Item administrators have the ability to edit and flag posts for reviewing, and user administrators have the ability to warn, flag, delete and block users from logging in as well as create new users from the user admin dashboard. Superusers who are logged in to the website have all privileges described above as well as a few others reserved to superusers like the ability to moderate other administrators.
