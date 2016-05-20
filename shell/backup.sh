#!/bin/bash

SHARED_DIR=/gpfs1/sales/salesconnect
SALES_DIR=/var/www/htdocs/sales/salesconnect

FS=/gpfs1/backup/
if [ $# -eq 0 ]
    then
        recipient_Build_No=$(grep -i 'sugar_build' $SALES_DIR/sugar_version.php | cut -d"'" -f2)
else
        recipient_Build_No=$1
fi

if [ ! -d "$FS" ]; then
	mkdir $FS
	if [[ $? -ne 0 ]]; then
		echo "[FATAL] Unable to create the directory $FS, please investigate"
		exit 1
	fi
	chmod 755 $FS
	if [[ $? -ne 0 ]]; then
		echo "[FATAL] Unable to change permissions on $FS, please investigate"
		exit 1
	fi


fi
# Tar.gz the backup
echo "Creating Salesconnect directory backup on $(hostname)"
tar cf - $SALES_DIR | gzip > $FS/propagate_$recipient_Build_No.tar.gz

if [ $? -ne 0 ]; then
    echo "[FATAL] The tar.gz of  $SALES_DIR didn't create correctly "
    exit -2
fi

# tar.gz the shared folders ( upload / cache / upload_notes)
echo "Creating shared folders directory backup on $(hostname)"
tar cf - $SHARED_DIR | gzip > $FS/sharedFolders_$recipient_Build_No.tar.gz
if [ $? -ne 0 ]; then
    echo "[FATAL] The tar.gz of $SHARED_DIR didn't create correctly "
    exit -2
fi


cp /var/www/htdocs/sales/salesconnect/config.php /var/www/htdocs/sales/backup_configs/config.php.$recipient_Build_No
if [ $? -ne 0 ]; then
    echo "[FATAL] apache permissions are probably not set , since someone was pulling root shennigans "
    exit -1
fi
cp /var/www/htdocs/sales/salesconnect/config_override.php /var/www/htdocs/sales/backup_configs/config_override.php.$recipient_Build_No
if [ $? -ne 0 ]; then
   echo "[FATAL] apache permissions are probably not set , since someone was pulling root shennigans "
   exit -1
fi
cp /var/www/htdocs/sales/salesconnect/batch/common/sfa.variables /var/www/htdocs/sales/backup_configs/sfa.variables.$recipient_Build_No
if [ $? -ne 0 ]; then
    echo "[FATAL] apache permissions are probably not set , since someone was pulling root shennigans "
	exit -1
fi



UH=/gpfs1/backup/upgrade_history/
mkdir -p $UH
. /home/apache/.profile
DB_PASS=$(grep -i 'db_password' $SALES_DIR/config.php | cut -d">" -f2 | sed s/[\',]//g)
echo "attempting to run $DB_PASS"
db2 connect to saleconn user sctid using $DB_PASS

db2 "export to $UH/$recipient_Build_No.ixf of ixf select * from sctid.upgrade_history"
# No error check here as there will always be warnings
