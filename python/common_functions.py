import subprocess


def run_command(command):
    p = subprocess.Popen(command, shell=True,
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT)
    (output, err) = p.communicate()
    if err is None:
        return output
    else:
        print "Something went wrong %r" % command
        return err