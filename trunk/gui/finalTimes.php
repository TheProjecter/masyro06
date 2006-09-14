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
				
				# Obtiene los tiempos finales.
				echo "<tr><td><b>Final times</b></td></tr>";
				$times = $masterPrx->getFinalTimes();
				$finalTimes = explode("\n", $times);
				
				foreach ($finalTimes as $elem) {
					echo "<tr><td>$elem</td></tr>";
				}						
				
			}
			catch (Ice_LocalException $ex) {
				print_r($ex);
			}
			
			echo "<META HTTP-EQUIV='refresh' CONTENT='10'; URL=$PHP_SELF'>";			
			
		?>		
		
		</table>
		
	</body>
	
</html>