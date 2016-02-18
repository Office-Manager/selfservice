<?php

if(!defined('sugarEntry'))define('sugarEntry', true);
require_once('/var/www/htdocs/sales/salesconnect/config_override.php');
error_reporting(-1);
$creds = $sugar_config['full_text_engine']['Elastic']['curl']['10005'];
$host = $sugar_config['full_text_engine']['Elastic']['host'];
$port = $sugar_config['full_text_engine']['Elastic']['port'];
$storage_dir = "/var/www/htdocs/selfservice/storage/";

$es_url = $_POST["es_url"];
$es_url = htmlspecialchars(trim($es_url));
$es_body = $_POST["es_body"];

$es_file = str_replace("/", "-" , $es_url);
$date = new DateTime();
$file_plain = $es_file.$date->getTimestamp();
$file_path_plain = $storage_dir.$file_plain;
$file_json = $es_file.$date->getTimestamp().".json";
$file_path_json = $storage_dir.$file_json;

$curl = curl_init();
$full = "https://".$host.":".$port."/".$es_url;
echo "<br>"; 



curl_setopt_array($curl, array(
    CURLOPT_RETURNTRANSFER => 1,
    CURLOPT_URL => $full,
    CURLOPT_USERPWD => $creds,
    CURLOPT_TIMEOUT => 15,
    // CURLOPT_VERBOSE => true,
    // CURLOPT_HEADER => true,
    CURLOPT_POSTFIELDS => $es_body,
    CURLOPT_SSL_VERIFYPEER => false,
    CURLOPT_SSL_VERIFYHOST => false,
    CURLOPT_CUSTOMREQUEST => "GET",
    CURLOPT_HTTPHEADER => array(
        'Content-Type: application/json',
        'Content-Length: ' . strlen($es_body)
    )
));

$output = curl_exec($curl);
curl_close($curl);



#echo $output;
file_put_contents($file_path_plain, $output);

shell_exec("python -m json.tool ".$file_path_plain." > ". $file_path_json);

if (strpos( $output,"No handler" ) !== false)
{
    ?>
		 <script>
		 window.alert('<?php echo $output; ?>');
		</script>
	<?php 
    exit;
}

if (filesize($file_path_json) < 500)
    { 
echo "<br>testing1 ";
$json = file_get_contents($file_path_json);
$json = trim(preg_replace('/\s+/', ' ', $json));
echo "entering file size less than 500 bytes";
echo "<br>".$json;
    ?>
		 <script>
		 window.alert('<?php echo $json; ?>');
		</script>
	<?php
   echo "<br>exiting1";
    exit;
}else {
    downloadFile($file_json,$storage_dir);
} 
   
    
function downloadFile($file, $storage_dir) {
	$file = trim($file);
    echo $file."<-- file name";
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
