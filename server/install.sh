#! /bin/bash
#apt-get install libapache2-mod-wsgi python-dev
#apt-get install apache2
#apt-get install python-pip
#
#sudo pip install flask
#sudo pip install flask_restful

#sudo pip install pip-autoremove
mkdir /var/www
mkdir /var/www/Flask
mkdir /var/www/Flask/Scheme
mkdir /var/www/Flask/Scheme/data
mkdir /var/www/Flask/Scheme/static

cp __init__.py /var/www/Flask/Scheme
cp schemeapp.wsgi /var/www/Flask
cp SchemeApp.conf /etc/apache2/sites-available
cp SchemePorts.conf /etc/apache2/conf-available
cp data/purchase_data.pkl /var/www/Flask/Scheme/data

sudo adduser $USER www-data
sudo chown root:root /var/www
sudo chown -R $USER:www-data /var/www/*
sudo chmod -R 755 /var/www

chmod g+rw /var/www/Flask/Scheme/data/purchase_data.pkl

a2ensite SchemeApp.conf
a2enconf SchemePorts.conf
systemctl reload apache2
systemctl restart apache2

