import sys
import time
import re
import zipfile

from common_functions import run_command


def find_line_number(full_path, time_unit, count, first_run, same_time,
                     hour_or_minute, pattern):
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
                if pattern.match(line):
                    try:
                        time_stamp = line.split()[3].split(":")
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
                        # should not be seen, print what causes and exit
                        print "This line caused a hissy fit %r" % (line)
                        sys.exit(-1)
                    count += 1
                count += 1
    return count


class LogFile(object):
    def __init__(self):
        # New time stamp needed so log file will be unique
        self.t_stamp = int(time.time())
        # hardcoded shizzle that won't expect to ever change
        self.log_directory = "/var/log/httpd/"
        # Type of log file passed from web GUI
        self.lookup_value = str(sys.argv[1])
        # Storage directory for the logs
        self.output_directory = "/var/www/htdocs/selfservice/storage/"

        if len(sys.argv) == 6:

            # Each log file uses a different logging format :/
            if self.lookup_value in ["sugarcrm"]:
                # regex - start of line must begin with
                # 3 characters followed by a literal white space
                # 3 characters followed by a literal white space
                # 2 digits followed by literal space
                # 00:00:00 format also allows 0000:00:00
                pattern = re.compile("^[a-zA-Z]{3}[\s][a-zA-Z]{3}[\s]"
                                     "[0-9]{2}[\s]"
                                     "[\d]{2,}[:][\d]{2}[:][\d]{2}")
            elif self.lookup_value in ["php"]:
                pattern = re.compile("Get the regex for php log file")
            else:
                print "stop trying to inject code"
                sys.exit(-1)
            # Get the latest log file
            # ls -ltr /dir/name | grep -i name | tail -1
            latest_file = run_command("ls -tr " + self.log_directory +
                                      " | grep -i " + self.lookup_value +
                                      " | tail -1 ").rstrip()
            # Make the new name for what the file sent via web GUI will be
            latest_txt = latest_file.replace(".log", "-" + str(self.t_stamp) +
                                             ".txt")
            self.pattern = pattern
            self.latest_txt = latest_txt
            self.full_path = self.log_directory + latest_file
            self.same_hour = int(sys.argv[2]) == int(sys.argv[4])
            self.same_minute = int(sys.argv[3]) == int(sys.argv[5])

        elif len(sys.argv) == 4:

            self.start_date = str(sys.argv[2])
            self.end_date = str(sys.argv[3])
        elif len(sys.argv) == 2:
            # Get the latest log file
            # ls -ltr /dir/name | grep -i name | tail -1
            self.latest_file = run_command("ls -tr " + self.log_directory +
                                           " | grep -i " + self.lookup_value +
                                           " | tail -1 ").rstrip()

    def get_start(self):
        count = 0
        count = find_line_number(self.full_path, int(sys.argv[2]), count, True,
                                 self.same_hour, True, self.pattern)
        count = find_line_number(self.full_path, int(sys.argv[3]), count, True,
                                 self.same_minute, False, self.pattern)
        return count

    def get_end(self, start_count):
        end_count = find_line_number(self.full_path, int(sys.argv[4]),
                                     start_count, False, self.same_hour,
                                     True, self.pattern)
        end_count = find_line_number(self.full_path, int(sys.argv[5]),
                                     end_count, False, self.same_minute, False,
                                     self.pattern)
        return end_count

    def create_file(self, start_count, end_count):
        run_command("sed '" + str(start_count + 1) + "," + str(end_count) +
                    "!d;' " + self.full_path + " > " + self.output_directory +
                    self.latest_txt)
        return self.latest_txt

    def get_dates_zip(self):
        run_command("touch -t \"" + self.start_date + "\" " +
                    self.log_directory + "touch_start")

        run_command("touch -t \"" + self.end_date + "\" " +
                    self.log_directory + "touch_end")

        hostname = run_command("hostname").rstrip()

        grab_files = run_command("find " + self.log_directory +
                                 " -type f -newer " + self.log_directory +
                                 "touch_start ! -newer " + self.log_directory +
                                 "touch_end" + "| grep -i " +
                                 self.lookup_value)
        grab_files = grab_files.split()
        zf = zipfile.ZipFile(self.output_directory + hostname +
                             str(self.t_stamp) + ".zip", mode="w")

        for _file in grab_files:
            zf.write(_file)
        zf.close()
        return hostname + str(self.t_stamp) + ".zip"

    def get_simple_log(self):
        latest_file = run_command("ls -tr " + self.log_directory +
                                  " | grep -i " + self.lookup_value +
                                  " | tail -1 ")
        if latest_file == "":
            return "defaultNotFound.txt"
        else:
            latest_txt = self.latest_file.replace(".log", "-" +
                                                  str(self.t_stamp) + ".txt")
            run_command("cp " + self.log_directory +
                        self.latest_file.rstrip() + " " +
                        self.output_directory + latest_txt)
            return latest_txt
