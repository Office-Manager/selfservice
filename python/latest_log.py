#!/usr/bin/python

import sys
import time
from common_functions import run_command


output_directory = "/var/www/htdocs/selfservice/storage/"
lookup_value = str(sys.argv[1]).rstrip()


time_stamp = int(time.time())

if lookup_value in ["SO_FAR_ALL_LOGS_ARE_IN_HERE"]:
    pass
else:
    log_directory = "/var/log/httpd/"

latest_file = ""

latest_file = run_command("ls -tr "+log_directory+" | grep -i "+ lookup_value + " | tail -1 ")
if latest_file == "":
    print "defaultNotFound.txt"
else:
    latest_txt = latest_file.replace(".log", "-"+str(time_stamp)+".txt")
    print latest_txt
    run_command("cp "+log_directory+latest_file.rstrip()+" "+output_directory+latest_txt)