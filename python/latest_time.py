#!/usr/bin/python

import sys
import time
import datetime
from common_functions import run_command

date = datetime.date.today()
if date.day < 10:
    TimeSplit = 4
else:
    TimeSplit = 3
def find_line_number(full_path, time_unit, count, first_run, same_time ,hour_or_minute):
    if hour_or_minute:
        # it's an hour
        field = 0
    else:
        # it's a minute
        field = 1
    with open(full_path) as f:
        for i, line in enumerate(f):
            if i < count:
                pass
            else:
                try:
                    time_stamp = line.split(" ")[TimeSplit].split(":")
                    time_stamp[field] = int(time_stamp[field])
                    if first_run or same_time:
                        if time_unit <= time_stamp[field]:
                            return count
                    else:
                        if hour_or_minute:
                            if time_unit == time_stamp[field]:
                                return count
                        else:
                            if time_unit < time_stamp[field]:
                                return count
                except:
                    pass
                count += 1
    return count
    
output_directory = "/var/www/htdocs/logs/storage/"

lookup_value = str(sys.argv[1]).rstrip()
start_hour = int(sys.argv[2])
start_minute = int(sys.argv[3])
end_hour = int(sys.argv[4])
end_minute = int(sys.argv[5])


time_stamp = int(time.time())

if lookup_value in ["sugarcrm"]:
    log_directory = "/var/log/httpd/"
latest_file = ""
latest_file = run_command("ls -tr "+log_directory+" | grep -i "+ lookup_value + " | tail -1 ").rstrip()
latest_txt = latest_file.replace(".log", "-"+str(time_stamp)+".txt")

full_path = log_directory+latest_file
count = 0
same_hour = False
same_minute = False

if start_hour == end_hour:
    same_hour = True
if start_minute == end_hour:
    same_minute = True
count = find_line_number(full_path, start_hour, count, True,same_hour, True)
count = find_line_number(full_path, start_minute, count, True, same_minute, False)
end_count = find_line_number(full_path, end_hour, count, False, same_hour, True)
end_count = find_line_number(full_path, end_minute, end_count, False, same_minute, False)

run_command("sed '"+str(count+1)+","+str(end_count)+"!d;' "+full_path+ " > "+output_directory+latest_txt)
print latest_txt

