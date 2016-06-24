# estus
Estus is an MVC package deployment tool for the Flask Microframework.


## System Requirements ##

**Operating System:** As of right now any UNIX like OS (Linux, OS X, BSD) is all that is supported.

**Python:** Tested working with Python 3.4+ on x86_64 systems.

**Environment:** So far very brief testing was done and permissions were preset to allow writes to all directories specified.

**Warning:** Not packaged for an actual install yet as it's VERY EARLY in development!!!

## How it Works ##
estus is my attempt to expedite building a web application in Flask. I took an MVC style approach to web building and it's worked out pretty well so far. Here's a brief description of how it works.

###### Usage ######

```bash
python3 estus.py testapp --design monolithic --orm sqlalchemy --log /var/log/estus/estus.log 
```

Now let's break down what each argument does

###### Arguments ######

**name** - The Application's name and most likely the working folder of the application is always the **FIRST** argument

**--path** - The location you intend to build the application in **WARNING** as of this writing it is very picky about permissions of said working directory, it must not already contain a project AND you need write and read access to it (similar to your home or Users/<user> folder if you're in OSX *(Optional: Defaults to <current working directory>/<name>)* 

**--design** - The design to pattern from. Flask's blueprint system allows one to build things in a very centralized structure (i.e. one static folder, one model folder, one controller folder to rule them all!), or a modular build where each application feels like its it's own entity (Similar to Django's system). Design specifies which of these approaches you want to use (*Optional: Defaults to monolithic)* **Options: monolithic, modular**

**--orm** - Everybody using an MVC Framework needs an ORM for their day to day database interactions. As of right now the only one available to use is SQLAlchemy, but I plan on looking into adding a few others (As of right now it merely preps the system for use with the ORM, it's your job to implement it). *(Optional: Defaults to sqlalchemy)* **Options: sqlalchemy**



# FAQs #

#### Why not just use Django, Pyramid, or TurboGears if you want an MVC framework for Python? ####

A: Because I like Flask's design and it's configuration over convention. However my main goal was to help circumvent the problem of development time inherent in developing an application whose framework gives you that much control. In other words I'm having my cake and eating it too!

#### Why Python 3? People still use Python 2 you Jerk! ####

A: Python 2 (to my knowledge) is feature frozen and is only receiving small vulnerability fixes and patches. Python 3 is the future, and I embrace it happily. I have **NO** plans to port this project to 2.

#### Okay, so why Python 3.4+ You madman?!? You must love living on the edge don't you?!? ####

A: I started really developing in 3.4.1 and have been keeping up with the changes of newer releases. But moreover some dependencies I use absolutely require features added in 3.4+

#### Do you really expect people to use this? ####

A: Maybe, if they find it useful great! If not then so be it. It has helped me in my line of work and if it helps other people then I say mission accomplished.
