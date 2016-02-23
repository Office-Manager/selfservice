cd /var/www/htdocs/
rm -f master.zip
wget http://bryantlab02.rtp.raleigh.ibm.com/public/master.zip
mkdir -p /var/www/htdocs/selfservice/
unzip -o master.zip -d /var/www/htdocs/selfservice/
chown -R apache:apache selfservice/
