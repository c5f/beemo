# Behavior Modeler for LIvES 

**Be[e]havior Modeler** (Beemo) is an AngularJS project designed to apply a [_k_-means clustering](http://en.wikipedia.org/wiki/K-means_clustering) analysis to extract and examine trends in participant and coach behavior within the [LIvES Project](http://ovarianlives.org).  Beemo utilizes a [Django REST Framework](http://django-rest-framework.org)/[Restangular](https://github.com/mgonto/restangular) backend and [d3.js](http://d3js.org) to visualize the data.

## Dependencies

Beemo relies heavily on several frameworks and package managers, but the system dependencies are as follows:

- [Python 2.7.5](https://www.python.org/download/releases/2.7.5/)
- [NodeJS](http://nodejs.org/)

### Installing Python Dependencies with [pip](http://pip.readthedocs.org/):

```shell
~ $ pip install -r requirements.txt
```

### Installing JavaScript Dependencies:

```shell
#               _
#  __ ___ _ __ (_)_ _  __ _   ___ ___  ___ _ _
# / _/ _ \ '  \| | ' \/ _` | (_-</ _ \/ _ \ ' \ _ _ _
# \__\___/_|_|_|_|_||_\__, | /__/\___/\___/_||_(_|_|_)
#                     |___/
```

## Setup

Coming soon...

## Running the Webserver

Because Beemo was built with [yeoman](http://yeoman.io/), staticfiles need to be compiled and moved where Django will recognize them before the webserver can be run.

```shell
# Run collectstatic to pull all staticfiles from the app directories into Django's staticfile location.
~/beemo $ python manage.py collectstatic

...

# Run the webserver
# Development
~/beemo $ python manage.py runserver

# Production
$ sudo service nginx restart
```
