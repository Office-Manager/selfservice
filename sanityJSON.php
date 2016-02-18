<?php
    header('Content-Type: application/json');
    chdir('/var/www/htdocs/sales/salesconnect');
    $value = shell_exec('php serverStatusJSON.php ');
    $value = substr($value,28);
    $value = substr($value,0,-1);
    echo $value;
?>
