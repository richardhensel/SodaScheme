
#apt-get install libapache2-mod-wsgi python-dev
#apt-get install apache2
#apt-get install python-pip
#
#pip install flask
#pip install flask_restful

mkdir /var/www
mkdir /var/www/Flask
mkdir /var/www/Flask/Scheme
mkdir /var/www/Flask/Scheme/data
mkdir /var/www/Flask/Scheme/static

cp __init__.py /var/www/Flask/Scheme
cp schemeapp.wsgi /var/www/Flask
cp SchemeApp.conf /etc/apache2/sites-available
cp data/purchase_data.pkl /var/www/Flask/Scheme/data

