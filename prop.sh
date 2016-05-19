cd /var/www/htdocs/
rm -f master.zip
if [ ! -f QueryLogging.txt ]; then
    touch QueryLogging.txt
fi
wget http://bryantlab02.rtp.raleigh.ibm.com/public/master.zip
if [ $? -ne 0 ];then
    echo "problem downloading the master.zip exiting"
    exit -1
fi
rm -rf /var/www/htdocs/selfservice/
mkdir -p /var/www/htdocs
unzip -o master.zip -d /var/www/htdocs
mv selfservice-master selfservice
chown -R apache:apache selfservice/
chown apache:apache QueryLogging.txt
