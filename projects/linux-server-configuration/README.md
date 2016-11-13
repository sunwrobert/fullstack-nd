# Linux Server Configuration
Configured a Linux virtual machine to properly serve the Item Catalog app I made earlier in the Nanodegree as well as other miscellaneous configurations.

## IP Address

35.162.72.187

## URL

http://ec2-35-162-72-187.us-west-2.compute.amazonaws.com/


## Software Installed
* Apache2
* PostgreSQL
* bleach
* flask-seasurf
* git
* github-flask
* httplib2
* libapache2-mod-wsgi
* oauth2client
* python-flask
* python-pip
* python-psycopg2
* python-sqlalchemy
* requests

## Configurations Made
* Update all currently installed packages
* Configure Automatic Security Updates
* Create a new user named `grader`
* Give `grader` sudo access
* Setup SSH Authentication and enforce it
* Change SSH Port to 2200 
* Disable remote root login
* Only allow connections for SSH, HTTP, and NTP
* Install and configure PostgreSQL
* Install and configure Apache2
* Deploy Item Catalog app

## References
https://www.digitalocean.com/community/tutorials/how-to-deploy-a-flask-application-on-an-ubuntu-vps