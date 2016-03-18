cd /var/www/htdocs/
rm -f master.zip
if [ ! -f QueryLogging.txt ]; then
    touch QueryLogging.txt
fi
wget http://bryantlab02.rtp.raleigh.ibm.com/public/master.zip
rm -rf /var/www/htdocs/selfservice/
mkdir -p /var/www/htdocs/selfservice/
unzip -o master.zip -d /var/www/htdocs/selfservice/
chown -R apache:apache selfservice/
chown apache:apache QueryLogging.txt
