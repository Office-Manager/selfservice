import sys
import time


number_argument_expected = 3
if (len(sys.argv)) != number_argument_expected:
    print("[FATAL] Exception: Invalid amount of arguments,please check the UCD "
          " process has " + str(number_argument_expected) + " arguments ")
    sys.exit(1)


# Application Name of ear being updated
app_name = str(sys.argv[0]).rstrip()

# type of application being updated - in case ear name different from what
#  expected
app_type = str(sys.argv[1]).rstrip()

# The ear file itself
app_file = str(sys.argv[2]).rstrip()


def confirm_application_name(app_name):
    installed_apps = AdminApp.list().splitlines()
    found = None
    for i in installed_apps:
        if i.find(app_name) >= 0:
            found = 1
    if not found:
        print("[FATAL] Exception : Application name " + app_name + " was not"
              " found on the server,  please check the UCD environment "
              "properties to confirm it's correct  ")
        sys.exit(1)

def get_application_properties(app):
    mods = AdminApp.listModules(app, '-server')
    (name, module, server) = mods.split('#')
    server_name = server.split('=')[-1]
    node_name = server.split('=')[-2].split(',', 1)[0]
    cell_name = server.split('=')[-3].split(',', 1)[0]

    cell_information = AdminConfig.list('Server').splitlines()
    cell_manager = None
    for i in cell_information:
        if i.find("dmgr") >= 0:
            cell_manager = i.split('/')[3]
    if cell_manager is None:
        cell_manager = cell_information[0].split('/')[3]

    was_version = AdminTask.getNodeBaseProductVersion('[-nodeName ' +
                                                      node_name + ']')
    return server_name, cell_name, node_name, cell_manager, was_version


def application_ready():
    result = AdminApp.isAppReady(app_name)
    i = 0
    while result == "false":
        # Wait 5 seconds before checking again
        i += 1
        time.sleep(5)
        print("[INFO] App has not deployed yet , re-checking attempt ", i)
        result = AdminApp.isAppReady(app_name)
        if i > 60:
            print("[FATAL] Exception: Application was not deployed after"
                  " 300 seconds! Exiting ")
            sys.exit(1)


def application_status():
    server_status = AdminControl.completeObjectName('type=Application,'
                                                    'name=' + app_name + ',*')
    return server_status


def application_state(command):
    AdminControl.invoke(
        'WebSphere:name=ApplicationManager,process=' + server_name + ''
        ',platform=proxy,node=' + node_name + ',version=' + was_version + ','
        'type=ApplicationManager,mbeanIdentifier=ApplicationManager,'
        'cell=' + cell_name + ',spec=1.0', command, '[' + app_name + ']',
        '[java.lang.String]')


def application_resync():
    AdminControl.invoke(
        'WebSphere:name=repository,process=nodeagent,platform=common,node=' +
        node_name + ',version=5.0,type=ConfigRepository,'
                    'mbeanIdentifier=repository,cell=' + cell_name +
        ',spec=1.0', 'refreshRepositoryEpoch')
    AdminControl.invoke(
        'WebSphere:name=cellSync,process=dmgr,platform=common,node=' +
        cell_manager + ',version=' + was_version + ',type=CellSync,'
        'mbeanIdentifier=cellSync,cell=' + cell_name + ',spec=1.0',
        'syncNode', '[' + node_name + ']', '[java.lang.String]')


def update_application():
    if app_type in ["spreadsheet"]:
        context_root = "-contextroot /ssload"
        map_module_str = "di.spreadsheetloader.webapp spreadsheetLoader.war"
    elif app_type in ["seedlist"]:
        context_root = ""
        map_module_str = '"SFA Seedlist Servlet" SaND-sfa-seedlist_WEB.war'
    elif app_type in ["emptoris"]:
        context_root = ""
        map_module_str = 'di.emptoris.webapp di.emptoris.webapp.war'
    elif app_type in ["crawler"]:
        context_root = "-contextroot /docrecommendations"
        map_module_str = "docrecommendations.web docrecommendations.war"
    else:
        sys.exit("[FATAL] Exception: Unsupported WAS App type selected.")

    update_parameters = """-operation update\
     -contents """ + app_file + """\
     -nopreCompileJSPs\
     -installed.ear.destination $(APP_INSTALL_ROOT)/""" + cell_name + """\
     -distributeApp\
     -nouseMetaDataFromBinary\
     -nodeployejb\
     -createMBeansForResources\
     -noreloadEnabled\
     -nodeployws\
     -validateinstall warn\
     -noprocessEmbeddedConfig\
     -filepermission .*\.dll=755#.*\.so=755#.*\.a=755#.*\.sl=755\
     -noallowDispatchRemoteInclude\
     -noallowServiceRemoteInclude\
     -asyncRequestDispatchType DISABLED\
     -nouseAutoLink\
     -noenableClientModule\
     -clientMode isolated\
     -novalidateSchema\
     """ + context_root + """\
     -MapModulesToServers [[ """ + map_module_str + """,WEB-INF/web.xml\
     WebSphere:cell=""" + cell_name + """,node=""" \
                        + node_name + """,server=""" + server_name + """ ]]\
     -MapWebModToVH [[ """ + map_module_str + """,WEB-INF/web.xml\
     default_host ]]
     """

    AdminApp.update(app_name, 'app', update_parameters)
    AdminConfig.save()

# Check the application name in the UCD properties actually exists
confirm_application_name(app_name)

# Flow of operations - shutdown down app , upgrade app , full resync,
#                      start app


(server_name, cell_name, node_name, cell_manager,
 was_version) = get_application_properties(app_name)


# If app running stop it
print("[INFO] Shutting down", app_name)
if application_status():
    application_state("stopApplication")
else:
    print("[INFO] app was off")
if application_status():
    print("[FATAL] Exception: The Application didn't stop as expected --"
          " This could be a larger problem ,far too general for me to guess")
    sys.exit(1)
# Sleep for 3 seconds as a pure safety on the off chance server is slow
time.sleep(3)

print("[INFO] Upgrade application ", app_name)
update_application()
time.sleep(3)

print("[INFO] checking if application fully deployed")
application_ready()

print("[INFO] App was deployed ,re-syncing")
application_resync()
time.sleep(3)

print("[INFO] starting application ", app_name)
application_state("startApplication")
if not application_status():
    print("[FATAL] Exception: The Application didn't start as expected --"
          " This could be a larger problem far to general for me too guess")
    sys.exit(1)

