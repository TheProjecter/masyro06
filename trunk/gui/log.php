<html>
	
	<head>
		<title>MASYRO: A Multi-Agent SYstem for Rendering Optimization</title>
	</head>

	<body>
		
		<table border="3">		
		
		<?php
			
			Ice_loadProfile();
		
			try {

				$masterPrx = $ICE->stringToProxy("master")->ice_checkedCast("::MASYRO::Master");				
				
				# Muestra el log.
				echo "<tr><td><b>Log</b></td></tr>";
				$log = $masterPrx->getLog();
				$logLines = explode("\n", $log);
				
				foreach ($logLines as $elem) {
					echo "<tr><td>$elem</td></tr>";
				}				
				
			}
			catch (Ice_LocalException $ex) {
				print_r($ex);
			}
			
			echo "<META HTTP-EQUIV='refresh' CONTENT='5'; URL=$PHP_SELF'>";			
			
		?>		
		
		</table>
		
	</body>
	
</html>