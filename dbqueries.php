<?php 

$work_dir= "/var/www/htdocs/selfservice";
$storage_dir = $work_dir."/storage/";

if(!defined('sugarEntry'))define('sugarEntry', true);
require_once('/var/www/htdocs/sales/salesconnect/config_override.php');
?>



<?php
$date = new DateTime();
$database = 'SALECONN';
$hostname = $sugar_config['db']['reports']['db_host_name'];
$port = $sugar_config['db']['reports']['db_port']; // also tried 50000

#$conn_string = "DRIVER={IBM DB2 ODBC DRIVER};DATABASE=$database;HOSTNAME=$hostname;PORT=$port;PROTOCOL=TCPIP;UID=$user;PWD=$password;";
#$conn_string = "DATABASE=SALECONN;HOSTNAME=svt4stdbydb.rtp.raleigh.ibm.com;PORT=50000;PROTOCOL=TCPIP;UID=sean01seanl01@tst.ibm.com;PWD=passw0rd";
$conn_string = "DATABASE=SALECONN;HOSTNAME=".$hostname.";PORT=".$port.";PROTOCOL=TCPIP;UID=sean01seanl01@tst.ibm.com;PWD=passw0rd";

$conn = db2_connect($conn_string, '', '');

#$sql = "select name from sctid.upgrade_history";
$message = "Dont use SELECT * type queries .The query attempted to use a data types which cannot be used in queries against a read-enabled HADR standby database.(LOB * )";
$query = $_POST["sql"];
$query = htmlspecialchars($query);
/*if (strpos($query," * ") !== false) {
?>
	<script>
	window.alert('<?php echo $message; ?>');
	</script>
<?php
exit;
}*/
$type = $_POST["sqltype"];
$format = $_POST["format"];
if ($type == "select"){
	$sql = $query;
} else {
$sql = "call SYSPROC.ADMIN_CMD('".$query."')";

}
$ip = $_SERVER['REMOTE_ADDR'];
$log_info = $date->format('Y-m-d H:i:s')."---".$ip."---".$sql."\n";
file_put_contents('/var/www/htdocs/QueryLogging.txt', $log_info, FILE_APPEND);

echo $log_info;
if ($conn) {
    $stmt = db2_prepare($conn, $sql);
   if ($stmt) {
      $success = db2_execute($stmt);
      if (!$success) {
         $result[]=  "exec errormsg1: " .db2_stmt_errormsg($stmt);
		 echo implode(' ',$result);
		 $stringy = implode(' ',$result); ?>
		 <script>
		 window.alert(' <?php echo $stringy; ?>');
		</script>
	  <?php 
	  }
	  else
	  {
			  while ($row = db2_fetch_array($stmt)) {
				  if ($format == "human"){
						$result[] = implode("		", $row);
					} else {
						$result[] = implode(",", $row);

					}
			  }
			
			$filename = 'db2_query.'.$date->getTimestamp().'.txt';
			file_put_contents ('/var/www/htdocs/selfservice/storage/'.$filename , implode("\r\n", $result));
			$handle = '/var/www/htdocs/selfservice/storage/'.$filename;
			fclose($handle);
			if ( 0 == filesize( $handle ) )
			{
				?>
				<script>
				window.alert('No results returned, Sorry ! \n It is possible you tried to query LOB data which is not allowed ');
				</script>
			<?php
			}
			else{
			echo "download";
			downloadFile($filename,$storage_dir);
			}
	  }
   } else {
         $result[]=  "exec errormsg2: " .db2_stmt_errormsg($stmt);
		 echo implode(' ',$result);
		 $stringy = implode(' ',$result); ?>
		 <script>
		 window.alert(' <?php echo "did you enter a query ?::".$stringy; ?>');
		</script>
	  <?php 
   }
   db2_close($conn);
   } else {
      echo "failed ".db2_conn_errormsg();
}
?>





<?php
function downloadFile($file, $storage_dir) {
	$file = trim($file);

	echo "<br>".$file;
	$output = shell_exec("whoami");
	echo "<br>whoami returns:".$output."<br>";  ## returns apache
	$output = shell_exec("ls -ltr ".$storage_dir.$file);
	echo "output is ls -ltr on log  :".$output."<br>";  ##-rw-r--r-- 1 apache apache 733295 Feb 24 05:59


    $fullPath = $storage_dir.$file;
	echo "<br>full path is ".$fullPath."<br>";
    if (file_exists($fullPath)) { ## doesn't work
		echo "the file exits";
		header('Content-Description: File Transfer');
		header('Content-Type: application/octet-stream');
		header('Content-Disposition: attachment; filename='.basename($storage_dir.$file));
		header('Content-Transfer-Encoding: binary');
		header('Expires: 0');
		header('Cache-Control: must-revalidate');
		header('Pragma: public');
		header('Content-Length: ' . filesize($storage_dir.$file));
		ob_clean();
		flush();
		readfile($storage_dir.$file);
		exit;
	}
	else {
		echo "the file wasn't found";
	}

}
?>