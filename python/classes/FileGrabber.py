import sys
import time
import os
import zipfile
import replace
from common_functions import run_command
from string import whitespace


class FileGrabber(object):
    def __init__(self):
        self.file_name = sys.argv[1].replace("\r", "\\")
        self.file_name = self.file_name.split("\\")
        self.hostname = run_command("hostname").rstrip()
        # Storage directory for the logs
        self.output_directory = "/var/www/htdocs/selfservice/storage/"
        self.not_found_directory = "/var/www/htdocs/sales/files-not-matched/"
        self.base_directory = ["/var/www/htdocs/sales/salesconnect/",
                               "/opt/freeware/etc/httpd/conf",
                               "/tempspace/ucd_temp/"]
        self.whitelist_files = ["/etc/openldap/ldap.conf",  "/opt/freeware/etc/php.ini"]
        # New time stamp needed so log file will be unique
        self.t_stamp = int(time.time())
        self.list_of_files = []
        os.chdir(self.output_directory)

    def check_input(self):
        for path in self.file_name:
            path = path.translate(None, whitespace)
            if path.startswith("/"):
                if path[:35] in self.base_directory:
                    if path.endswith("/ALL"):
                        if os.path.exists(path[:-3]):
                            self.get_directory(path[:-3])
                    else:
                        if os.path.exists(path):
                            self.list_of_files.append(path)
                        else:
                            self.file_not_found(path)
                elif path[:28] in self.base_directory:
                    if path.endswith("/ALL"):
                        if os.path.exists(path[:-3]):
                            self.get_directory(path[:-3])
                    else:
                        if os.path.exists(path):
                            self.list_of_files.append(path)
                        else:
                            self.file_not_found(path)
                elif path in self.whitelist_files:
                    self.list_of_files.append(path)
                else:
                    self.file_not_found(path)
            else:
                if path == "ALL":
                    self.get_directory(self.base_directory[0])
                if path.endswith("/ALL"):
                    if os.path.exists(self.base_directory[0]+path[:-3]):
                        self.get_directory(self.base_directory[0]+path[:-3])
                elif os.path.exists(self.base_directory[0]+path):
                    self.list_of_files.append(self.base_directory[0]+path)
                else:
                    self.file_not_found(path)
        if len(self.list_of_files) == 1:
            base_name = os.path.basename(str(self.list_of_files[0]))
            dir_name = os.path.dirname(str(self.list_of_files[0]))
            if self.check_blacklist(base_name):
                base_name += ".scrubbed"
            run_command("cp " + dir_name+"/"+base_name + " " +
                        self.output_directory + base_name)
            print base_name
        else:
            self.create_zip()

    def file_not_found(self, path):
        path = path.replace("/", "-")
        if not os.path.exists(self.not_found_directory):
            os.makedirs(self.not_found_directory)
        not_found = (self.not_found_directory + path)

        open(not_found, 'w')
        self.list_of_files.append(not_found)

    def create_zip(self):
        zf = zipfile.ZipFile(self.output_directory + self.hostname +
                             str(self.t_stamp) + ".zip", mode="w")
        unique_files = []
        for _file in self.list_of_files:
            if self.check_blacklist(_file):
                unique_files.append(_file + ".scrubbed")
            else:
                unique_files.append(_file)
        unique_files = list(set(unique_files))
        for _file in unique_files:
            zf.write(_file)
        zf.close()
        print self.hostname + str(self.t_stamp) + ".zip"

    def get_directory(self, directory):
        grab_files = run_command("find " + directory + "* -prune -type f ")
        grab_files = grab_files.splitlines()
        for _file in grab_files:
            self.list_of_files.append(_file)

    def check_blacklist(self, file_name):
        if os.path.basename(file_name) in ["config.php", "config_override.php",
                                           "sfa.variables"]:
            replace.replaced_files()
            return True

    def return_files(self):
        self.check_input()
