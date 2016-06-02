<?php
    header('Content-Type: application/json');

    if (file_exists("/var/www/htdocs/sales/salesconnect/custom/service/IBMSanityCheck/serverStatusJSON.php")) {
        $value = shell_exec('php custom/service/IBMSanityCheck/serverStatusJSON.php');
        $value = substr($value,28);
         }
    else {
	    $value = shell_exec('php serverStatusJSON.php');
		$value = substr($value,28);
         }
    $value = substr($value,0,-1);
    echo $value;
?>
