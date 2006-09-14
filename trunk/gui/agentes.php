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
				$states = $masterPrx->showAgentStates();
				$agentStates = explode("\n", $states);

				# Muestra el estado de los agentes.
				echo "<tr><td><b>Agent</b></td><td><b>Status</b></td></tr>";
				foreach ($agentStates as $elem) {
					list($agent, $state) = split(":", $elem);
					echo "<tr><td>$agent</td><td>$state</td></tr>";
				}							
				
			}
			catch (Ice_LocalException $ex) {
				print_r($ex);
			}
			
			echo "<META HTTP-EQUIV='refresh' CONTENT='1'; URL=$PHP_SELF'>";			
			
		?>		
		
		</table>
		
	</body>
	
</html>