import os


def replace_passwords(file_path, triggers):
    config = open(file_path, "r+")
    file_path += ".scrubbed"
    scrubbed = open(file_path, "wt")
    lines = config.readlines()
    for line in lines:
        if not "=" in line:
            scrubbed.write(line)
            continue
        config_line = line.split("=")
        if any([i.upper() in config_line[0].upper() for i in triggers]):
            if "config_override.php" in file_path:
                line = line.replace(str(config_line[1]), "\'replace me\'; \n")
            elif "config.php" in file_path:
                if "," in config_line[1]:
                    append = ","
                else:
                    append = ";"
                line = line.replace(str(config_line[1]), "> \'replace me\' " +
                                    append+" \n")
            elif "sfa.variables" in file_path:
                line = line.replace(str(config_line[1]), "replace_me \n")
            scrubbed.write(line)
        else:
            scrubbed.write(line)
    config.close()
    scrubbed.close()

password_triggers_configs = ["\'password\'", "\'db_password\'", "site_url",
                             "host_name", "gadget_path", "SAbsolutePath",
                             "dojoHost", "directHost", "proxiedHost",
                             "proxiedHost", "\'list\'", "ispClientHostURL",
                             "10005", "\'Elastic\'][\'host\'", "publishUser",
                             "soapURL", "httpKey", "SAML_Issuer", ]
password_triggers_sfa = ["password", "Passwd", " username", "db2url",
                         "IST_SERVER"]


def replaced_files():
    os.chdir("/var/www/htdocs/sales/salesconnect")
    # Run the 3 files which need to be scrubbed
    replace_passwords("config_override.php", password_triggers_configs)
    replace_passwords("config.php", password_triggers_configs)
    replace_passwords("batch/common/sfa.variables", password_triggers_sfa)

if __name__ == '__main__':
    replaced_files()

