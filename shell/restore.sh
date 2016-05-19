#!/bin/bash

SHARED_DIR=/gpfs1/sales/salesconnect
SALES_DIR=/var/www/htdocs/sales/salesconnect

FS=/gpfs1/backup/
CONFIG=${2,,}



if [ $# -eq 0 ]
    then
        echo "You must enter a parameter to specify the build number you want to restore
For example to restore sharedFolders_r33_sev1_40-2.tar.gz please use
./restore.sh r33_sev1_40-2"
    exit 1
else
        Build_No=$1
fi
if [$(ls $FS | grep -i $Build_No".tar.gz" | wc -l ) -ne 2 ];then
    echo "The parameter you entered should only find 2 matches .You shouldn't see this message"
    echo "run this command to try and debug"
    echo "ls $FS | grep -i $Build_No.tar.gz"
    exit 2
fi


echo "Deleting the salesconnect directory"
rm -rf $SALES_DIR

# Ultra rare but a file can be created by an already kicked off cron job so double delete to make sure
rm -rf $SALES_DIR
if [ $? -ne 0 ]; then
    echo "Everything was not deleted, please check the permissions on $SALES_DIR "
    exit -3
fi

echo "deleting the shared cache directory"
rm -rf $SHARED_DIR
# Ultra rare but a file can be created by an already kicked off cron job so double delete to make sure
rm -rf $SHARED_DIR
if [ $? -ne 0 ]; then
    echo "Everything was not deleted, please check the permissions on $SALES_DIR "
    exit -3
fi


BUILDS=$(ls $FS | grep -i $Build_No".tar.gz")
for i in $BUILDS ; do
echo "untaring $i"
gzip -dc $FS/$i | tar -xf -
if [[ $? -ne 0 ]]; then
    echo "The untar of $i image failed"
    exit -1
fi
done

UH=/gpfs1/backup/upgrade_history/
mkdir -p $UH
. /home/apache/.profile
DB_PASS=$(grep -i 'db_password' $SALES_DIR/config.php | cut -d">" -f2 | sed s/[\',]//g)
db2 connect to saleconn user sctid using $DB_PASS
db2 delete from sctid.upgrade_history
db2 delete from sctid.upgrade_history
db2 "import from $UH/$Build_No.ixf  of ixf insert into sctid.upgrade_history"


if [ $CONFIG = "true" ]; then
    echo "replacing the config files with the ENV_BASE ones"
    cp /var/www/htdocs/sales/backup_configs/ENV_BASE.config.php /var/www/htdocs/sales/salesconnect/config.php
    if [ $? -ne 0 ]; then
        echo "[FATAL] apache permissions are probably not set , since someone was pulling root shennigans "
        exit -1
    fi
    cp /var/www/htdocs/sales/backup_configs/ENV_BASE.config_override.php /var/www/htdocs/sales/salesconnect/config_override.php
    if [ $? -ne 0 ]; then
        echo "[FATAL] apache permissions are probably not set , since someone was pulling root shennigans "
        exit -1
    fi
    cp /var/www/htdocs/sales/backup_configs/ENV_BASE.sfa.variables /var/www/htdocs/sales/salesconnect/batch/common/sfa.variables
    if [ $? -ne 0 ]; then
        echo "[FATAL] apache permissions are probably not set , since someone was pulling root shennigans "
        exit -1
    fi
fi
