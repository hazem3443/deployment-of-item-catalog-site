# :dizzy:final-project:sparkles:
this is a deployed version of **ITEM CATALOG**:cupid: App for the final evaluation grader has access with private key file **grader** to access the deployed **VPS** :broken_heart:

# **Grader info**:boom:
you have to download this repository :v: using the command shell
```
git clone https://github.com/hazemkhaledmohamed/Final-Project 
```
then to login to the server you need to type 
```
ssh grader@142.93.205.132 -p 2200 -i grader
```
then type the **passphrase** :: **hazem**:raised_hands: then you will be prompeted to access the server's shell **CLI** (command line interface)

# How Did i Deployed this site :question::pray:
## First the Instructions for SSH access to the instance
* first you need to install some packages such as those 'sudo apt-get install apache' 
* create account on any web hosting service such as [Digital-Ocean](https://www.digitalocean.com/):muscle: or [AWS](https://aws.amazon.com/):clap:
* then create a VPS with CLI access to enable you using command line with root access and password:skull:
* first:ear: create a public and private keys using ssh key-gen tool with any command line interface such as Git or Powershell:nose:
**Note**::trollface:
private key shouldn't included but for evaluation i decided to attach it here

* then create a new User **grader** with command ``` sudo adduser grader ``` 
* then give him the sudo access ```touch /etc/sudoers.d/grader```
* vim ```/etc/sudoers.d/grader```, type in ```grader ALL=(ALL:ALL) ALL```, save and quit
* copy puplic key content to file in this directory ``` /.ssh/authorized_keys ```
* Open your terminal and type in ``` chmod 644 ~/.ssh/grader.pub ``` and ``` chmod 700 ~/.ssh ```
* reload SSH:snake: using `service ssh restart`
* try loggin:mushroom:g as grader with private key in my case i am using git so simply open the directory where the file exists in the shell and type the folloing command ``` ssh grader@142.93.205.132 -p 2222 -i grader ``` note we will change that port later
* Give the grader the permission to sudo:mushroom:

## Update all currently installed packages:seedling::partly_sunny:
	sudo apt-get update
	sudo apt-get upgrade

## Change the SSH port from 22 to 2200
* Use `sudo vim /etc/ssh/sshd_config` and then change Port 22 to Port 2200 , save & quit.
* Reload SSH using `sudo service ssh restart`

## Configure the Uncomplicated Firewall (UFW):no_bell:

Configure the Uncomplicated Firewall (UFW) to only allow incoming connections for SSH (port 2200), HTTP (port 80), and NTP (port 123)

	sudo ufw allow 2200/tcp
	sudo ufw allow 80/tcp
	sudo ufw allow 123/udp
	sudo ufw enable 
## Configure the local timezone to UTC:partly_sunny:
* Configure the time zone `sudo dpkg-reconfigure tzdata`
* It is already set to UTC.

## Install and configure Apache to serve a Python mod_wsgi application :confetti_ball:
* Install Apache `sudo apt-get install apache2`
* Install mod_wsgi `sudo apt-get install python-setuptools libapache2-mod-wsgi`
* Restart Apache `sudo service apache2 restart`

## Install and configure PostgreSQL:phone:
* Install PostgreSQL `sudo apt-get install postgresql`
* Check if no remote connections are allowed `sudo vim /etc/postgresql/9.3/main/pg_hba.conf`
* Login as user "postgres" `sudo su - postgres`
* Get into postgreSQL shell:telephone_receiver: `psql`
* Create a new database named catalog  and create a new user named catalog in postgreSQL shell
	
	```
	postgres=# CREATE DATABASE catalog;
	postgres=# CREATE USER catalog;
	```
** Set a password for user catalog which is **hazem123**:mega::satellite:
	
	`postgres=# ALTER ROLE catalog WITH PASSWORD 'hazem123';` 
	
* Give user "catalog" permission to "catalog" application database:unlock:
	
	```
	postgres=# GRANT ALL PRIVILEGES ON DATABASE catalog TO catalog;
	```
* Quit postgreSQL `postgres=# \q`
* Exit from user "postgres" 
	
	```
	exit
	```
 
## Install git, clone and setup your Catalog App project.:flashlight:
* Install Git using `sudo apt-get install git`
* project tree should be like this





![proect Tree](https://i.pinimg.com/originals/76/16/e3/7616e3356d08b233e8c3716b8bf8349b.png)
* Clone the Catalog to the Fist FlaskApp directoy and name it FlaskApp as the following ``` it clone https://github.com/hazemkhaledmohamed/Final-Project FlaskApp ```
* Install pip `sudo apt-get install python-pip`
* Use pip:low_brightness: to install dependencies `sudo pip install -r requirements.txt`
* Install psycopg2 `sudo apt-get -qqy install postgresql python-psycopg2`
* Create database schema `sudo python database_setup.py`

## Configure and Enable a New Virtual Host :bath:
* Create FlaskApp.conf to edit: `sudo nano /etc/apache2/sites-available/FlaskApp.conf`
* Add the following lines of code to the file to configure the virtual host. 	
	```
	<VirtualHost *:80>
                ServerName 142.93.205.132
                ServerAdmin 142.93.205.132
                WSGIScriptAlias / /var/www/FlaskApp/flaskapp.wsgi
                <Directory /var/www/FlaskApp/FlaskApp/>
                        Order allow,deny
                        Allow from all
                </Directory>
                Alias /static /var/www/FlaskApp/FlaskApp/static
                <Directory /var/www/FlaskApp/FlaskApp/static/>
                        Order allow,deny
                        Allow from all
                </Directory>
                ErrorLog ${APACHE_LOG_DIR}/error.log
                LogLevel warn
                CustomLog ${APACHE_LOG_DIR}/access.log combined
	</VirtualHost>
	```
* Enable the virtual host with the following command: `sudo a2ensite FlaskApp`

## Create the .wsgi File :triangular_ruler:
* Create the .wsgi File under /var/www/FlaskApp: 
	
	```
	cd /var/www/FlaskApp
	sudo nano flaskapp.wsgi 
	```
* Add the following lines of code to the:musical_score: flaskapp.wsgi file:
	
	```
	#!/usr/bin/python
	import sys
	import logging
	logging.basicConfig(stream=sys.stderr)
	sys.path.insert(0,"/var/www/FlaskApp/")

	from FlaskApp import app as application
	application.secret_key = 'SUPER_SECRET_KEY'
	```

## Restart Apache:gem:
* Restart Apache:trophy: `sudo service apache2 restart `

then go to browser and type [142.93.205.132](http://142.93.205.132) and let the magic happen

# **you can follow these links to deploy your site i find it very usefull and helped me alot to deploy mine**
* [Flask-with-digitalOcean](https://www.digitalocean.com/community/tutorials/how-to-deploy-a-flask-application-on-an-ubuntu-vps)
* [Apache-internal-server-Error](https://www.digitalocean.com/community/questions/500-internal-server-error-how-can-i-fix-this-this-website-was-supposed-to-be-a-christmas-present)
* [StackOverflow-PathIssue](https://stackoverflow.com/questions/7302619/operationalerror-operationalerror-unable-to-open-database-file-none-none)
* [Apache-ServerGuide](https://help.ubuntu.com/lts/serverguide/httpd.html)
* [DataBase-Server-Setup-using-Postgresql](https://o7planning.org/en/11325/installing-and-configuring-postgresql-database-on-ubuntu-server)

also you can Follow Me on Facebook [Facebook Profile](https://www.facebook.com/hazem.khaled.3386585):saxophone:
