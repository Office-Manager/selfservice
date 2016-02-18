
<div id="modules_results">
    <?php
        if(!defined('sugarEntry'))define('sugarEntry', true);
        require_once('/var/www/htdocs/sales/salesconnect/sugar_version.php');
        require_once('/var/www/htdocs/sales/salesconnect/config.php');
        require_once('/var/www/htdocs/sales/salesconnect/config_override.php');

        $database = $sugar_config['dbconfig']['db_name'] ;
        $user = $sugar_config['dbconfig']['db_user_name'] ;
        $password = $sugar_config['dbconfig']['db_password'] ;
        $conn = db2_connect($database, $user, $password);

        // Sugar modules
        echo "<table border=0 align=\"center\">";
        echo "<th>Module Name</th><th>Version</th>";
        if ($conn) {
           $sql = " select name,version from sctid.upgrade_history";
           $stmt = db2_prepare($conn, $sql);
           if ($stmt) {
              $result = db2_execute($stmt);
              if (!$result) {
                 echo "exec errormsg: " .db2_stmt_errormsg($stmt);
              }
              while ($row = db2_fetch_array($stmt)) {
                echo "<tr>";
                echo "<td> {$row[0]} </td><td> {$row[1]} <td>";
                echo "</tr>";
              }
              echo "</table>"; 
           } else {
                 echo "exec errormsg: " . db2_stmt_errormsg($stmt);
           }
           db2_close($conn);
           } else {
              echo "faild ".db2_conn_errormsg();
        }
    ?>
</div>