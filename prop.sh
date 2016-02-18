cd /var/www/htdocs/
rm -f selfservice.tar
wget http://bryantlab02.rtp.raleigh.ibm.com/public/selfservice.tar
tar -xf selfservice.tar
chown -R apache:apache selfservice/
