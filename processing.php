<?php

$work_dir= "/var/www/htdocs/selfservice";
$storage_dir = $work_dir."/storage/";
$log_name = $_POST["log_name"];
$log_name = htmlspecialchars($log_name);
switch($_POST["log_type"]){
    case latest_log:
        $command = "python ".$work_dir."/python/log_dispenser.py"." ".$log_name;
        $command = escapeshellcmd($command);
        $output = shell_exec($command);
        downloadFile($output,$storage_dir);
        break;
    case latest_time:
        $start_hour = $_POST["start_hour"];
        $start_minute = $_POST["start_minute"];
        $end_hour = $_POST["end_hour"];
        $end_minute = $_POST["end_minute"];
        $command = "python ".$work_dir."/python/log_dispenser.py"." ".$log_name." ".$start_hour." ".$start_minute." ".$end_hour." ".$end_minute;
        $output = shell_exec($command);
        downloadFile($output,$storage_dir);
        break;
    case latest_dates:
        $start_date = str_replace('-','',$_POST["start_date"]."0001");
        $end_date = str_replace('-','',$_POST["end_date"]."2359");
        $command = "python ".$work_dir."/python/log_dispenser.py"." ".$log_name." ".$start_date." ".$end_date;
        $output = shell_exec($command);
        downloadFile($output,$storage_dir);

}
?>

<?php
function downloadFile($file, $storage_dir) {
	$file = trim($file);
    $fullPath = $storage_dir.$file;
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