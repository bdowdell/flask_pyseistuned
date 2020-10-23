# PySeisTuned<sup>2.0</sup>
A Flask / Python-based web app version of PySeisTuned<sup>1.0</sup>.

The original version, PySeisTuned<sup>1.0</sup>, is a Python / PyQT5 GUI application that runs locally in a desktop environment. The new version, PySeisTuned<sup>2.0</sup>, is a web app that makes it even easier for users to explore seismic tuning from the comfort of the world-wide-web!

## Getting started
If you want to run PySeisTuned<sup>2.0</sup> locally, there are a few things you need to do first. I'll walk you through the steps now!

### 1) Install pipenv
For this project, I chose to use pipenv to create a virtual environment. If you don't already have pipenv installed, here's what you do:

`$ pip install pipenv`

pipenv is a really cool tool that basically combines pip and virtualenv into one streamlined utility that makes managing virtual environments and packages really straightforward. I opted to go with pipenv instead of conda for this project because it just seemed a little more straightforward. I think I prefer conda for data science type projects and pipenv for application development, but I digress ...

### 2) Clone this repository
Next, you need to clone this repository on your local machine. If you want to make contributions, then you will also want to create your own branch. To clone the repository, simply use the green button above labelled "Code" to copy the repository URL to the clipboard. Then in the terminal:

`$ git clone https://github.com/bdowdell/flask_pyseistuned.git`

### 3) Set up the flask_pyseistuned virtual environment
Now that you have the repository cloned on your local machine, you need to install the flask_pyseistuned virtual environment:

`$ pipenv install`

pipenv will use the Pipfile and Pipfile.lock to set up the virtual environment. Once it is set up, launch the environment:

`$ pipenv shell`

And when you are done, you can exit the environment by:

`$ exit`

### 4) Set flask-specific environment variables
Before you can run the flask_pyseistuned web app, you need to set several flask-specific environment variables from inside the repository directory. 

*Note: If you are working from within an IDE such as VS Code or PyCharm, I suggest you set these environment variables using the IDE's integrated terminal.*

First, set the FLASK_APP environment variable:

`$ export FLASK_APP=pyseistuned.py`

set the FLASK_CONFIG environment variable:

`$ export FLASK_ENV=development`

and set the FLASK_CONFIG environment variable:

`$ export FLASK_DEBUG=1`

The FLASK_APP variable tells flask what application it is supposed to run and the FLASK_ENV variable specifies you will be running in a development mode so that the visual debugger is available in the web browers when things go wrong.

### 5) Launch a virtual email server
To test email sending functionality on the contact page, a virtual email server needs to be launched. Open a new terminal or new tab in a terminal and:

`$ python -m smtpd -c DebuggingServer -n localhost:8025`

You won't see anything happen. The virtual email server has launched and is now listening for an email to be sent. Return to terminal where you previously set the flask environment variables. There are two more environment variables which need to be set for the virtual mail server.

First, set the MAIL_SERVER variable:

`$ export MAIL_SERVER=localhost`

and then set the MAIL_PORT variable:

`$ export MAIL_PORT=8025`

At this point you are now ready to run the application!

### 6) Launch the flask web app
To launch the web app, simply type the command:

`$ flask run`

You should see a message that states:

```
 * Serving Flask app "pyseistuned/pyseistuned" (lazy loading)
 * Environment: development
 * Debug mode: on
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: xxx-xxx-xxx
```
This means that the web app is running! Click the link and it will open in your default web browser.
 
