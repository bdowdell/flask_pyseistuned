# PySeisTuned<sup>2.0</sup>
A Flask / Python-based web app version of PySeisTuned<sup>1.0</sup>.

The original version, PySeisTuned<sup>1.0</sup>, is a Python / PyQT5 GUI application that runs locally in a desktop environment. The new version, PySeisTuned<sup>2.0</sup>, is a web app that makes it even easier for users to explore seismic tuning from the comfort of the world-wide-web!

## Citing PySeisTuned<sup>2.0</sup>
If you use PySeisTuned<sup>2.0</sup> as part of a publication, please include a citation in the references section:

Dowdell, B.L., 2020, PySeisTuned2.0, [https://www.pyseistuned.com/](https://www.pyseistuned.com/), accessed MM DD, YYYY.

Publications which use PySeisTuned<sup>2.0</sup> will be featured on the page.

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

`$ export FLASK_CONFIG=development`

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

#### *Note:*

All environmental variables can be placed inside a `.env` file instead of exporting them; however, `FLASK_APP` 
needs to either be set by the user or placed inside a file such as `~/.bashrc` or `~/.profile`. The reason for this is 
that flask needs to know what application it should be pointed at prior to invoking `flask run` after which point the 
app will load all environmental variables from `.env` if the file exists. The `.env` file is not included in source 
control because several variables are sensitive and should not be shared publicly, so it is up to the user to create 
this file, if desired. The easiest way to do this is using your editor of choice inside the `flask_pyseistuned` root 
directory:

```
$ cd
$ echo "export FLASK_APP=pyseistuned.py" >> .bashrc
$ source ~/.bashrc
$ cd /path/to/flask_pyseistuned
$ vim .env
```

### 6) Run unit tests & check coverage
This project uses the Python unittest package to run automated unit tests. To run the tests, run the command after 
setting the environmental variables above:

`$ flask test`

If all the tests pass, each test should be followed by "... OK" with a final "OK" at the end.

In addition to using unittest, this project also uses the Python Coverage module to report code coverage. To generate 
a coverage report at the same time as running the unit tests, add the `--coverage` flag:

`$ flask test --coverage`

Passing the `--coverage` option to `flask test` will result in both a coverage report in the terminal as 
well as the creation of an html version of the report in the directory `htmlcov` created after the initial coverage run.

Alternatively, coverage can also be ran independently of running the unit tests by running:

```
$ coverage run -m unittest discover
$ coverage html app/*.py app/main/*.py
```

The first command re-runs all the unit tests and the second generates a nicely formatted HTML report that is very useful 
in visually seeing how much of the code is or isn't being tested. Once the second command completes running, a new 
directory is created in the project called `htmlcov` and you can view the report by opening the file `index.html` in a 
web browser.

### 7) Launch the flask web app
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
