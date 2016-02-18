#!/usr/bin/python

import sys
import zipfile
import time
from common_functions import run_command


output_directory = "/var/www/htdocs/selfservice/storage/"
lookup_value = str(sys.argv[1])
start_date = str(sys.argv[2])
end_date = str(sys.argv[3])

if lookup_value in ["sugarcrm"]:
    log_directory = "/var/log/httpd/"

run_command("touch -t \""+start_date+"\" "+log_directory+"touch_start")
#touch_end =
run_command("touch -t \""+end_date+"\" "+log_directory+"touch_end")
hostname = run_command("hostname").rstrip()

grab_files = run_command("find "+log_directory+" -type f -newer " +
                         log_directory + "touch_start ! -newer " +
                         log_directory + "touch_end" +
                         "| grep -i " + lookup_value)
grab_files = grab_files.split()
time_stamp = int(time.time())
zf = zipfile.ZipFile(output_directory+hostname+str(time_stamp)+".zip", mode="w")
for _file in grab_files:
    zf.write(_file)
zf.close()
print (hostname+str(time_stamp)+".zip")


def main():
    test = LogFile()
    print test.get_dates_zip()

if __name__ == '__main__':
    main()