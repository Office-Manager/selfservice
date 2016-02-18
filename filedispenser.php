<?php
$work_dir= "/var/www/htdocs/selfservice";
$storage_dir = "/var/www/htdocs/selfservice/storage/";
$filePaths = $_POST["filePaths"];
$filePaths = htmlspecialchars($filePaths);
    
    $command = "python ".$work_dir."/python/file_grabber.py"." \"".$filePaths."\"";
    $command = escapeshellcmd($command);
    echo "<br>Test-1:".$command."<br>";

    $output = shell_exec($command);
    echo "this is the output<br>";
    echo $output;
    echo "<br>";
    $file = trim($storage_dir.$output);
    echo $file;
    echo gettype($file);
    if ( 0 == filesize($file))
    {
        ?>
        <script>
        window.alert('No results returned, Sorry ! ');
        </script>
        <?php
    }
    else{
    echo "download";
    downloadFile($output,$storage_dir);
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