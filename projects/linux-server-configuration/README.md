# Linux Server Configuration
Configured a Linux virtual machine to properly serve the Item Catalog app I made earlier in the Nanodegree as well as other miscellaneous configurations.

## IP Address

35.162.72.187

## URL

http://ec2-35-162-72-187.us-west-2.compute.amazonaws.com/


## Software Installed
* Apache2
* PostgreSQL

Installed from the requirements.txt file from the Item catalog app

* Flask==0.10.1
* Flask-HTTPAuth==3.2.1
* Jinja2==2.7.2
* Markdown==2.6.7
* MarkupSafe==0.18
* PyYAML==3.10
* SQLAlchemy==0.8.4
* SecretStorage==2.0.0
* Werkzeug==0.9.4
* argparse==1.2.1
* configobj==4.7.2
* gunicorn==19.6.0
* html5lib==0.999
* httplib2==0.9.2
* oauth==1.0.1
* oauth2client==4.0.0
* psycopg2==2.4.5
* requests==2.2.1
* rsa==3.4.2
* urllib3==1.7.1
* wadllib==1.3.2
* wsgiref==0.1.2

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