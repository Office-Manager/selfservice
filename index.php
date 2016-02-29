<?php
if(!defined('sugarEntry'))define('sugarEntry', true);
require_once('/var/www/htdocs/sales/salesconnect/sugar_version.php');
require_once('/var/www/htdocs/sales/salesconnect/config.php');
require_once('/var/www/htdocs/sales/salesconnect/config_override.php');

?>
<html>
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
    <title>Nobody likes collecting logs</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/2.1.4/jquery.min.js"></script>
    <script type="text/javascript" src="js/bootstrap.min.js"></script>
    <link href="css/bootstrap.css" rel="stylesheet" type="text/css">
    <link rel="stylesheet" type="text/css" href="css/view.css" media="all">
    <script type="text/javascript" src="js/selfservice.js"></script>
</head>
<body id="main_body">
<iframe name="hiddenFrame" class="hide"></iframe>
<div class="container">
  <h1>SalesConnect Self Service<sup>Make your admins love you!</sup></h1>
  <p>Select your utility from the options below.</p>
  <div class="pill-menu">
    <ul class="nav nav-pills">
      <li class="active"><a data-toggle="pill" href="#logdispenser">
        <span class="glyphicon glyphicon-stats" aria-hidden="true"></span>
          Log Dispenser</a></li>
      <li><a data-toggle="pill" href="#dbqueries">
        <span class="glyphicon glyphicon-search" aria-hidden="true"></span>
          Database Queries</a></li>
      <li><a data-toggle="pill" href="#filedispenser">
        <span class="glyphicon glyphicon-file" aria-hidden="true"></span>
          File Dispenser</a></li>
    <li><a data-toggle="pill" href="#eschecker">
        <span class="glyphicon glyphicon-piggy-bank" aria-hidden="true"></span>
          ES Checker</a></li>
    </ul>
  </div>
<div class="tab-content">
  <div id="logdispenser" class="tab-pane fade in active">
      <div class="form_description">
        <form action="processing.php" method="post" target="hiddenFrame" class="formClass"/>
        <div class="content">
          <h4>Log Dispenser <sup>" - Because it's soul destroying collecting logs "</sup></h4>
          <p> Select your desired log file. </p>
            <ul>
            <li>
                <div id="dropdownChoice">
                <label class="description" for="log_name">Select the log file you want</label>
                <select  id="log_name" name="log_name" onchange="hideRadio(value)">
                    <option value="sugarcrm"  >Sugarcrm.log</option>
                    <option value="php"  >php.log</option>
                    <option value="cron"  >cron.log</option>
                    <option value="PMSE"  >PMSE.log</option>
                    <option value="dipubEngine"  >dipubEngine.log</option>
                    <option value="dipubLogicHooks"  >dipubLogicHooks.log</option>
                    <option value="diASLogicHooks"  >diASLogicHooks.log</option>
                    <option value="ibmlpde"  >ibmlpde.log</option>
                    <option value="access_log"  >access log</option>

                </select>
            </li>

            <li>
            <div id="radioChoice" >
                <input type="radio" name="log_type" value="latest_log" id="latest_log"  onclick="showHide(1)"/>
                <span id="latest_log_label">Latest log</span><br>
                <input type="radio" name="log_type" value="latest_time" id="latest_time" onclick="showHide(2)"/>
                 <span id="latest_time_label">Latest Log (between specific times)</span><br>

                <p class="guidelines" id="guide_1"><small>
                    Latest log will give you the latest sugarcrm.log in it's entirety<br>
                    Latest log between specific times will give you the log with only the entries appearing between the times<br>
                    Logs from specific dates will give you a zip of the log files which were last written to on those dates

                    </small></p>
            </div></li>

            <li>
            <div id="timeChoice" class="hidden_time" style="">
          <p>Please remember the time on the server is <?php echo date("H:i:s" , time()); ?>
          <br> Don't expect log times to be different than this </P>

                <p>Time to begin log trim</p>
                <select name="start_hour">
                    <?php for($x=1;$x<=23;$x++) { ?>
                        <option value="<?= $x ?>"<?= (date("H") == $x ? ' selected="selected"' : '') ?>><?= $x ?></option>
                    <?php } ?>
                </select>
                <select name="start_minute">
                    <option value="00">00</option>
                    <option value="15">15</option>
                    <option value="30">30</option>
                    <option value="45">45</option>
                </select>
                <p>Time to end log trim</p>
                <select name="end_hour">
                    <?php for($x=1;$x<=23;$x++) { ?>
                        <option value="<?= $x ?>"<?= (date("H") == $x ? ' selected="selected"' : '') ?>><?= $x ?></option>
                    <?php } ?>
                </select>
                <select name="end_minute">
                    <option value="00">00</option>
                    <option value="15">15</option>
                    <option value="30">30</option>
                    <option value="45">45</option>
                </select>
                <p class="guidelines" id="guide_1"><small>Enter the timestamps on the log you'd like returned
                  <br />
                    if you receive a blank file it's quite possible there was nothing reported between those times
                  </small>
               </p>
            </div>
            </li>
                    </li>
                    <br />
                    <input type="submit" class="btn btn-primary">
        </div>
            </ul>
      </form>
    </div>
  </div>
  <div id="dbqueries" class="tab-pane fade">
    <form action="dbqueries.php" method="post" target="hiddenFrame" class="formClass" id="dbqueriesForm"/>
      <div class="content">
        <h4>Database Queries <sup>" - Because it's heart crushing using Sametime for database queries " </sup></h4>
        Choose the type of the SQL statement you'd like to run. <br />
        Multiple queries not supported.</p>
          <div class="form-group" id="query-options">
            <div class="col-md-5">
  		      <p> <strong> Query Type </strong> </p>
            <div class="radio-inline">
              <label><input type="radio" name="sqltype" id="sqlSelect" value="select" checked>SELECT</label>
            </div>
            <div class="radio-inline">
              <label for="sqltype">
                <input type="radio" name="sqltype" id="sqlMeta" value="describe">Meta Data</label>
            </div>
          </div>
			    <div class="col-md-7">
      			<p><strong> Output format </strong></p>
      		  <div class="radio-inline">
      		     <label for="sqltype">
                 <input type="radio" name="format" id="format" value="human" checked>Human readable format</label>
                </div>
      		  <div class="radio-inline">
              <label><input type="radio" name="format" id="format" value="CSV">CSV format</label>
            </div>
          </div>
        </div>
        <div class="form-group" style="padding-top: 20px;">
          <textarea class="form-control" rows="5" name="sql" id="sql">SELECT [column] FROM [schemaOwner.tablename]</textarea>
          <br />
          <a class="btn btn-primary" id="clearSQL">Clear</a>
          <input type="submit" class="btn btn-primary">
        </div>
      </div>
    </form>
  </div>
  <div id="filedispenser" class="tab-pane fade">
    <form action="filedispenser.php" method="post" target="hiddenFrame" class="formClass" id="filedispenserForm"/>
      <div class="content">
        <h4>File Dispenser <sup>" - i like WinSCP ... but I don't like it that much. "<sup></h4>
        <p> New line separated file paths</p>
        <div class="form-group">
              <p><strong>Example usage</strong></p>
              <p><strong>To get all files in a directory:</strong></p>
              /var/www/htdocs/sales/salesconnect/ALL  or    ALL<br>
              /var/www/htdocs/sales/salesconnect/cache/ALL  or    cache/ALL<br>
              <br>
              <p><strong> To get specific files </strong><p>
              /var/www/htdocs/sales/salesconnect/folder-name/specific_file.php   or  folder-name/specific_file.php

              <p> multiple queries can be ran at once <p>

          <textarea class="form-control" rows="5" name="filePaths" id="filepath"></textarea>
          <br />
          <input type="submit" class="btn btn-primary">
        </div>
      </div>
    </form>
  </div>
    <div id="eschecker" class="tab-pane fade">
    <form action="eschecker.php" method="post" target="hiddenFrame" class="formClass" id="escheckerForm"/>
      <div class="content">
        <h4>ES checker <sup style="font-size: 58%">" - Sheep, like all wool-bearing animals, instinctively travel north, where it's colder, and they won't be so stuffy "<sup></h4>
        <p>'http://&lt;ES_HOST&gt;:ES_PORT/ <strong>&lt;'url'&gt;</strong> -d <strong>&lt;'request_body'>&gt;</strong> </p>
        <p> Please enter the <strong>'url'</strong>  and the <strong>'request_body'</strong> below</p>
        <div class="form-group">
              <p><strong>url</strong></p>
          <textarea class="form-control" rows="1" name="es_url" id="es_url"></textarea>
              <br>
             <p><strong>request_body</strong> (optional)</p>
          <textarea class="form-control" rows="5" name="es_body" id="es_body"></textarea>
          <br />
          <input type="submit" class="btn btn-primary">
        </div>
      </div>
    </form>
  </div>
</div>
</div>


      <?php

        $database = $sugar_config['dbconfig']['db_name'] ;
        $user = $sugar_config['dbconfig']['db_user_name'] ;
        $password = $sugar_config['dbconfig']['db_password'] ;
        $conn = db2_connect($database, $user, $password);
        $connections = $sugar_config['connections_http_base_url'];
        $ieb_url = $sugar_config['ieb_connections_base_url'];
		    $cluster = $sugar_config['cluster_name'];

        // Sugar version
        echo("<div class=\"twisties\">".
                "<div class=\"panel panel-primary\">".
                  "<div class=\"panel-heading\">Server info <span class=\"glyphicon glyphicon-hand-left pull-right\"></span></div>".
                "<div class=\"panel-body\">".
                    "<table border=0 align=\"center\">".
                      "<td align=\"center\">Hostname</td> <td><strong>".shell_exec("hostname")."</strong></td>".
                     "</tr><tr>".
                      "<td align=\"center\">Sugar Version</td> <td><b><span id=\"build_version\">$sugar_build</span></b></td>".
                     "</tr><tr>".
                      "<td align=\"center\">Connections Server</td> <td><b><span id=\"connections_server\">$connections</span></b></td>".
                     "</tr><tr>".
                      "<td align=\"center\">IEB Connections Server</td> <td><b><span id=\"ieb_url\">$ieb_url</span></b></td>".
                   "</tr></table>".
                 "</div>".
               "</div>".
             "</div>");

       // Sanity Tests
       echo('<div class="twisties">'.
               '<div class="panel panel-primary">'.
                 '<div class="panel-heading">Sanity results <span class="glyphicon glyphicon-hand-left pull-right"></span></div>'.
               '<div class="panel-body">'.
                 '<div id="sanity_results">'.
                   '<div id=\"sanity_loader\">'.
                       '<p align="center"><img src="images/loader.gif" /></p>'.
                       '<p align="center">Loading sanity results...</p>'.
                    '</div>'.
                  '</div>'.
                '</div>'.
              '</div>'.
            '</div>');

        // Database modules
        echo('<div class="twisties">'.
                '<div class="panel panel-primary">'.
                  '<div class="panel-heading">Database modules <span class="glyphicon glyphicon-hand-left pull-right"></span></div>'.
                '<div class="panel-body">'.
                  '<div id="modules_results">'.
                    '<div id="modules_loader">'.
                       '<p align="center"><img src="images/loader.gif" /></p>'.
                       '<p align="center">Loading db2 modules... </p>'.
                    '</div>'.
                  '</div>'.
                 '</div>'.
               '</div>'.
             '</div>');

?>
</div>
</body>
</html>
