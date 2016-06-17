import subprocess
import sys
import os
import time


def run_command(command):
    p = subprocess.Popen(command, shell=True,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT)
    (output, err) = p.communicate()
    if err is None:
        return output
    else:
        print("Something went wrong %r" % command)
        return err


def find_ini_files():
    ini_files = []
    path_to_ini = os.getcwd() + "/iniFiles/"
    for f in os.listdir(path_to_ini):
        if f.endswith(".ini"):
            ini_files.append(path_to_ini + f)
    return ini_files


def get_orchs_on_system(g1_list, g2_list):
    ini_files = find_ini_files()
    # This will list all the orchs currently on the machine , both machines
    # should have identical orchs
    run_command("php ciHelper.php listOrchs %s | tail -n +8 > tmp.listedOrchs"
                % ini_files[0])
    orchs = open("tmp.listedOrchs", "r+")
    lines = orchs.readlines()

    g2_found = match_orchs(g2_list, lines, True)
    g1_found = match_orchs(g1_list, lines, True)
    combined = g1_found + g2_found
    others_found = match_orchs(combined, lines, False)

    return g2_found, g1_found, others_found


def match_orchs(listed, lines, normal_order):
    tmp_list = []
    if normal_order:
        for orch in listed:
            for line in lines:
                if orch in line:
                    tmp_list.append(line.rstrip())
    else:
        for line in lines:
            if not any([i in line for i in listed]):
                tmp_list.append(line.rstrip())
    return tmp_list


def get_status(group, f, status_wanted):
    status_check = run_command("php ciHelper.php listStatus %s " % f)
    naughty_orchs = group
    print("Status wanted is %s " % status_wanted)
    for line in status_check.splitlines():
        for orch in group:
            if orch in line:
                status = line.split("=")
                if status[1].strip() in status_wanted:
                    if status[0].strip() in naughty_orchs:
                        naughty_orchs.remove(status[0].strip())
                    else:
                        print("found %s to be in state %s" % (
                            status[0], status[1]))
                else:
                    print("Orch: %s   Status: %s  Status Wanted: %s"
                          % (status[0], status[1], status_wanted))

    return naughty_orchs


def run_operation(group, command):
    ini_files = find_ini_files()
    exit_bool = False
    append = "s"
    naughty_orchs = []
    if command == "stop":
        append = ""

    for f in ini_files:
        if command in ["stop"]:
            naughty_orchs = get_status(group, f, ["stopped", "undeployed"])
            for orch in naughty_orchs:
                print("running %s on %s" % (command, orch))
                run_command("php ciHelper.php %sProject%s %s %s"
                            % (command, append, f, orch))
        elif command == "undeploy":
            print("undeploy part")
            naughty_orchs = get_status(group, f, ["undeployed"])
            if naughty_orchs:
                print("running %s on %s" % (command, f))
                run_command("php ciHelper.php %sProject%s %s"
                            % (command, append, f))
        elif command == "start":
            naughty_orchs = get_status(group, f, ["running"])
            for orch in naughty_orchs:
                print("running %s on %s" % (command, orch))
                run_command("php ciHelper.php %sProject%s %s %s"
                            % (command, append, f, orch))
        elif command == "wipe":
            run_command(
                "php ciHelper.php wipeBox %s override" % f)
        elif command == "wipe_specific":
            for i in group:
                run_command("php ciHelper.php wipeBox %s %s override" % (f, i))
        elif command == "publish":
            run_command(
                "php ciHelper.php %sProject%s %s %s override "
                % (command, append, f, group))

    if command == "stop":
        if naughty_orchs:
            print("waiting 30 seconds for all orchs in the group to stop")
            time.sleep(30)
            print("30 seconds complete")

    if command in ["stop", "undeploy", "start"]:
        # Do 5 attempts at it, if they're all success exit.
        # If they haven't stopped run a cancel
        i = 0
        while i < 5:
            i += 1
            for f in ini_files:
                if command in ["stop"]:
                    naughty_orchs = get_status(
                        group, f, ["stopped", "undeployed"])
                    if naughty_orchs:
                        print("Creating tmp.check because of %s"
                              % naughty_orchs)
                        open("tmp.check", 'a').close()
                elif command in ["undeploy"]:
                    naughty_orchs = get_status(group, f, ["undeployed"])
                    if naughty_orchs:
                        print("Creating tmp.check because of %s"
                              % naughty_orchs)
                        open("tmp.check", 'a').close()
                elif command in ["start"]:
                    naughty_orchs = get_status(group, f, ["running"])
                    if naughty_orchs:
                        print("Creating tmp.check because of %s"
                              % naughty_orchs)
                        open("tmp.check", 'a').close()
                if os.path.isfile("tmp.check"):
                    print("sleeping for 30 seconds tmp.check found")
                    time.sleep(30)
                    os.remove("tmp.check")
                else:
                    if command in ["stop"]:
                        print("all Orchs %sped exiting loop" % command)
                    else:
                        print("all Orchs %sed exiting loop" % command)
                    exit_bool = True
                    i = 5

        if command == "stop":
            if not exit_bool:
                i = 0
                while i < 5:
                    i += 1
                    for f in ini_files:
                        for orch in group:
                            if command in ["stop"]:
                                print("%sing %s with cancel override."
                                      % (command, orch))
                            run_command(
                                "php ciHelper.php %sProject%s %s %s  cancel"
                                % (command, append, f, orch))
                            group = get_status(group, f,
                                               ["stopped", "undeployed"])
                    time.sleep(30)
                naughty_orchs = get_status(group, f, ["stopped", "undeployed"])
                if naughty_orchs:
                    print("Orchestration %s haven't stopped" % naughty_orchs)
                    sys.exit(-1)


group1_orchs = ["BAT_SFA_SyncCampaign",
                "BluemixContactTaskCreate",
                "CCMSBackendSearch",
                "CCMSChangeLogController",
                "CCMSChangeLogWorkerStage0",
                "CCMSChangeLogWorkerStage1",
                "CCMSChangeLogWorkerStage2",
                "CCMSChangeLogWorkerStage3",
                "CCMSInteractiveSearch",
                "CCMSSitePubPopulateStagingDB",
                "CCMSSitePubUpdateStage1",
                "CCMSSitePubUpdateSugar",
                "CCMSUnqualifiedSiteController",
                "ISTManager",
                "IntegrationErrorProcess",
                "MonitorBusinessPartnerUpdates",
                "MonitorSiebelContactChanges_AG",
                "MonitorSiebelContactChanges_AP",
                "MonitorSiebelContactChanges_EU",
                "OneTEAMReclaim",
                "OneTEAMSync",
                "PublishCron_Contact",
                "PublishCron_Oppty",
                "Publish_DB_to_MQ_Contact",
                "Publish_DB_to_MQ_Oppty",
                "RequestServiceHealthCheck",
                "RequestSubmissionProxy",
                "SFAContactAndOpptySyncProxy",
                "SSI_SFA_SyncProduct",
                "SyncProxyPopulateStagingDB",
                "SyncResponseStatus_clone",
                "UpdateSiteInCCMS",
                "SellerAdjustmentPublish",
                "MonitorGPPOpptyDelete",
                "GPPRepubRequestProxy",
                "GPPSync",
                "TaskOperations",
                "SpreadsheetLoader",
                "TargetPublish"
                ]

group2_orchs = ["CreateSiteInCCMS",
                "CCMSSiteCountryMap",
                "ClientDeleteRelatedRecords",
                "CreateCRMClientsInSFA",
                "CreateCRMContactsInSFA",
                "CCMSCMRLock",
                "CCMSRemoveSCKey",
                "CCMSRequestService",
                "LoadBalancer",
                "SugarRequestWebService",
                "ErrorService"
                ]

select_orchs = []


def shutdown_orchs(g1_list, g2_list):
    g1_found, g2_found, others_found = get_orchs_on_system(g1_list, g2_list)
    ini_files = find_ini_files()

    # specific orchestration to stop before both groups on T1 and Prod only
    for f in ini_files:
        print(f)
        run_command(
            "php ciHelper.php stopProject %s "
            "RequestServiceHealthCheck_To_Prod_T1 cancel" % f)
    # give sleep period just to be safe
    print("Sleeping for 5 seconds")
    time.sleep(5)

    # Group 1 have to be shutdown first.
    print("Stopping the first group of orchs")
    run_operation(g1_found, "stop")

    # Stop the second group of orchs
    print("Stopping the second group of orchs")
    run_operation(g2_found, "stop")

    # Stop anything not contained in the lists
    print("Stopping the remaining group of orchs")
    run_operation(others_found, "stop")

    # Undeploy the orchs so they're in a state to be started
    undeploy_orchs(g1_list, g2_list)


def undeploy_orchs(g1_list, g2_list):
    # Undeploy all orchs , order doesn't matter for this to run all orchs
    # would already have been stopped
    g1_found, g2_found, others_found = get_orchs_on_system(g1_list, g2_list)
    group = g1_found + g2_found + others_found
    run_operation(group, "undeploy")


def startup_orchs(g1_list, g2_list):
    g1_found, g2_found, others_found = get_orchs_on_system(g1_list, g2_list)
    ini_files = find_ini_files()
    # specific orchestration to stop before both groups on T1 and Prod only
    for f in ini_files:
        print(f)
        run_command(
            "php ciHelper.php startProject %s "
            "RequestServiceHealthCheck_To_Prod_T1 cancel" % f)
    # give sleep period just to be safe
    print("Sleeping for 5 seconds")
    time.sleep(5)

    print("starting the second group of orchs")
    run_operation(g2_found, "start")

    print("starting the first group of orchs")
    run_operation(g1_found, "start")

    print("starting the remaining group of orchs")
    run_operation(others_found, "start")


def wipe_orchs():
    # All orchs should be assumed stopped at this stage.
    print("Wiping all orchs from system")
    run_operation("", "wipe")


def publish_orchs():
    # modify the ini_files to point to the newest pars
    if len(sys.argv) > 2:
        build_label = str(sys.argv[2]).rstrip()
    else:
        print("Incorrect amount of arguments given")
        sys.exit(-1)
    print("Publishing new orchestrations")
    # Changing the Time Stamp to include the full build label.
    # With the option of specific orchestrations I feel it's
    # important to know which Build the orchestration came from
    time_stamp = "_" + build_label
    run_operation(time_stamp, "publish")


def upgrade_orchs(g1_list, g2_list):
    wipe_orchs()
    publish_orchs()


def wipe_specific(select_orchs):
    run_operation(select_orchs, "wipe_specific")


def publish_specific(select_orchs):
    downloaded_pars = []
    deleted_pars = []
    tmp_pars = []
    path_to_par = "CastIron/archives/"
    for par in os.listdir(path_to_par):
        if par.endswith(".par"):
            downloaded_pars.append(par)
    for i in downloaded_pars:
        for j in select_orchs:
            if j in i:
                tmp_pars.append(i)
    print tmp_pars
    deleted_pars = list(set(downloaded_pars) - set(tmp_pars))
    for i in deleted_pars:
        os.remove(path_to_par + i)
    publish_orchs()


def upgrade_specific(g1_list, g2_list, select_orchs):
    g1_found, g2_found, others_found = get_orchs_on_system(g1_list, g2_list)
    group = g1_found + g2_found + others_found
    select_orchs_found = []
    select_orchs_publish = []
    for i in group:
        for j in select_orchs:
            if j in i:
                select_orchs_found.append(i)
                select_orchs_publish.append(j)

    wipe_specific(select_orchs_found)
    publish_specific(select_orchs_publish)


def main():
    process = str(sys.argv[1]).rstrip()
    if len(sys.argv) == 4:
        my_string = str(sys.argv[3])
        select_orchs = my_string.split(",")
    if process == "Shutdown":
        shutdown_orchs(group1_orchs, group2_orchs)
    elif process == "Startup":
        startup_orchs(group1_orchs, group2_orchs)
    elif process == "Upgrade":
        upgrade_orchs(group1_orchs, group2_orchs)
    elif process == "specific_upgrade":
        upgrade_specific(group1_orchs, group2_orchs, select_orchs)


if __name__ == '__main__':
    main()
