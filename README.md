# Cyber Security Base 2021 - Project I


This is a course project for the Cyber security base 2021 MOOC course. The purpose of the project is to demonstrate some serious security flaws and describe how to fix them.

My project is a simple voting app that can be used by students when deciding the next day’s school lunch. The app's home page shows the poll that has been added today, and polls can be added, removed and edited by admin only. Students should also not see past or future polls, and they should be able to vote only the current poll.

Make sure that you have python3 and django installed.
To run the application navigate to the project folder and run:
>python3 manage.py runserver
  
admin panel:
>localhost:8000/admin  
>user:admin password:admin  

app:
>localhost:8000/lunch_app  

The requirements for this project were to implement security flaws from the OWASP top ten list. I used the 2021 version:
https://owasp.org/www-project-top-ten/

## FLAW 1 - IDENTIFICATION AND AUTHENTICATION FAILURES 
https://github.com/viltas/CSB-project-I/blob/d4935ec83fd2d756c49c7eb4bf20b45c383cb450/project/project/settings.py#L88

Currently user accounts and logging in are used for administration purposes only, but the security of the admin account is very weak. The software accepts very weak passwords, and currently the administrator password is the same as the username (admin / admin). The application allows dangerously short and popular passwords. Therefore, it would be very easy for an attacker to guess the administrator's password and access the maintenance panel to view and edit the information intended to be secret.

Django offers options to improve the strength of your passwords:  
https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators  
By re-enabling AUTH_PASSWORD_VALIDATORS = [...] in setting.py file, the application will use those password validators again. Then the application will notify the user if they are choosing a password that is too weak.


## FLAW 2 - CRYPTOGRAPHIC FAILURE
https://github.com/viltas/CSB-project-I/blob/d4935ec83fd2d756c49c7eb4bf20b45c383cb450/project/project/settings.py#L23  

The settings.py file contains the SECRET_KEY value that is used in cryptographic signing. It is used for salting hashes and generating csrf tokens, for example. SECRET_KEY needs to be kept secret, so pushing it into the github repository is an enormous security risk. 

To fix this problem a new SECRET_KEY should be generated. After that the new key could be used via an environment variable that would then be referenced in the settings.py file. So instead of using a hard coded key it could be loaded from a file:
with open('/secret.txt') as f:
    SECRET_KEY = f.read().strip()
The file containing the SECRET_KEY value must be added to .gitignore so it won’t be uploaded into the repository again.



## FLAW 3 - BROKEN ACCESS CONTROL
https://github.com/viltas/CSB-project-I/blob/master/project/lunch_app/models.py

Users should only be able to vote for the current poll on the front page of the app. At a glance, this seems to be the case. Only today's survey is displayed on the home page. However, a smart attacker will quickly notice that the address of the details page for each query contains the primary key for that query. And that's not all: primary keys have sequential numbering. Thus, with a little manipulation of the address, it is easy to find the voting pages of later as well as previous polls, and through them it is possible to manipulate the polls before they are officially visible.

Preventing or at least complicating such an attack can be done by making the primary keys/id:s of Lunches random. Long enough numbers are difficult or even impossible to guess. For example, the Django random-id model could be used to do this. It is a django module that provides a base class for Django models that gives them a randomly generated primary key id.  
https://pypi.org/project/django-random-id-model/

A more complicated and perhaps more of a certain way would be to compare the server time to the time specified for the query, and then choose whether or not to display the contents of the details page. For example, a conditional page could lead to a 404 view when a user requests a Lunch that is not yet visible. For added security, it might be wise to implement both security measurements.

## FLAW 4 - SECURITY MISCONFIGURATION
https://github.com/viltas/CSB-project-I/blob/d4935ec83fd2d756c49c7eb4bf20b45c383cb450/project/project/settings.py#L26

The app's debug mode is currently on. The application displays detailed error messages to the user in the event of problems. Such debug messages are very useful when developing a program, but should not be accessed by the end user or a potential attacker. Debug messages allow an attacker to obtain information about the operation of an application and thus better prepare for an attack. Fortunately, solving the problem is easy. Debug mode can be turned off in the settings.py file:
DEBUG = True



## FLAW 5 - INSECURE DESIGN
https://github.com/viltas/CSB-project-I/blob/d4935ec83fd2d756c49c7eb4bf20b45c383cb450/project/lunch_app/templates/lunch_app/detail.html#L17  
https://github.com/viltas/CSB-project-I/blob/d4935ec83fd2d756c49c7eb4bf20b45c383cb450/project/lunch_app/views.py#L28

Lastly, I would like to highlight the insecure design category. Secure development requires use of threat modeling, secured component libraries and tools. When designing a secure app, threats and security flaws should be evaluated constantly. A good example of insecure design could be that if there’s a well-known security risk with an established solution, one would not use it.

In my project the case is that the protection against csrf attacks offered by Django is not in use. Detail.html file should contain a csrf token, and csrf protection should not be overridden in views.py. CSRF used to be its own OWASP category, but it was removed due to increased use of secure frameworks and content management systems. Nowadays it is quite easy to minimize the danger of CSRF attacks, and because of that, refusing the protection offered by Django would be careless and generally very bad planning. CSRF ​​the vulnerability can be removed by adding the csrf_token to the details.html file, and removing csrf_exempt from the views.py file.

But what if the application still contains vulnerabilities that have not been noticed yet? This could be overcome by testing the application. It is an insecure design that no tests have been written for the application. With unit testing it might have been possible to notice, for example, that the details page allows users to view information that should not be visible. Further development of the application may also create new security vulnerabilities, and previous functionalities may operate unexpectedly later. In such situations, effective testing will help detect security issues before they have time to cause problems.
