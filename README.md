# UrSpace

INTRODUCTION
UrSpace Rentals Cooperation system is created in the Django framework to allow users to book and use working rooms or spaces at our locations throughout Glasgow city. There are multiple login pages, for users, operators, and managers. 
New users can navigate to our sign-up page instead of login.
Regular users can book rooms at available locations and time slots and view user profile. 
Operators can track rooms, repair and update defective reports and change room availability.
Managers can track all operator info and orders.

REQUIREMENTS

To run and deploy the project smoothly, make sure the following requirements are met:

➢ You have Python3 but versions no newer than 3.10 installed on your system(3.9 is recommended), as all of the codings are done in python only.

➢ You have Node.js installed on your system

➢ You must have a good internet connection.

➢ You need to have at least one of these text editors (or IDEs) installed on your system: Visual
Studio Code, Pycharm, Anaconda (Jupyter or Spyder), or Atom.

Now, these are the basic software requirements, other than these, you just need to follow the instructions provided below to make sure the project works flawlessly on your system.

INSTRUCTIONS

If you want to run it locally, please follow these steps:

After you’ve met the basic requirements, unzip and open the source code folder named "UrSpace"  onto your text editor/IDE. For quick view of the system, we already save data in db.sqlite3. So to run this project, simply follow these instructions:

1. In the folder, you can see a file ‘requirements.txt’, this file contains all the modules that we used in python to work on the project, you’ll have to install them as well. To install all the modules in one go, open the python terminal, in that, open the project folder, and run the following command:


      pip install -r requirements.txt


This command will install all the required modules.

and you’ll be good to go.

2. Now, to run the project on your localhost, enter the following command on your terminal:

         python manage.py runserver

Now, after this command, if you open localhost:8000 on your web browser, it should open our login page. 

To create a new user, you can simply register with information needed. We have these default users to quickly go through UrSpace:

In http://urspace.onrender.com: 
email: lpy@outlook.com, password: 123456
In http://urspace.onrender.com/admin/:
username: admin, password: 123456

To create a Manager User, enter the following command on your terminal:

      python manage.py createsuperuser

After entering username and password, you will be able to login as a manager in manager login page. For quick going through, you can use default manager user:
Manager User:
username: admin, password: 123456

If you want to deploy this system on Render web server, follow these instructions:

1. create a new repository on Github and update the code

2. open render.com and create a new project.

3. in project settings, update start command:

         python manage.py collectstatic --noinput && gunicorn UrSpace.wsgi:application --bind 0.0.0.0:$PORT


4. choose source code UrSpace in your Github repositories and choose deploy last commit

Now you should be able to view this project on http://urspace.onrender.com: 



