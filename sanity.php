<div id="sanity_table">
<?php
        // Sanity Tests
		
		if(!defined('sugarEntry'))define('sugarEntry', true);
		require_once('/var/www/htdocs/sales/salesconnect/config_override.php');
        
        echo "<table border=0 align=\"center\">";
        echo "<th>Sanity Test results</th>";
        echo "<tr>";
		$cluster = $sugar_config['cluster_name'];
		if ($cluster == "SC4IBM")
		{
		
            chdir('/var/www/htdocs/sales/salesconnect/');
            if (file_exists("/var/www/htdocs/sales/salesconnect/custom/service/IBMSanityCheck/serverStatusJSON.php")) {
                $value = shell_exec('php custom/service/IBMSanityCheck/serverStatusCLI.php');
                $value = substr($value,17);
                }
            else {
				$value = shell_exec('php serverStatusCLI.php');
				$value = substr($value,17);
                }
			echo "<td>".nl2br(htmlentities($value))."</td>"; // for HTML as output, with <br/> for newlines
				
		}else {
				echo "<td> Sozzles we don't run Sanity on SC4BP instance anymore !</td>";
		}
		echo "</table>";

?>
</div>
