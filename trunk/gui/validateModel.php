<html>

	<head>
		<meta http-equiv="Content-Language" content="en-us">
		<meta http-equiv="Content-Type" content="text/html; charset=windows-1252">
		<title>MASYRO: A Multi-Agent SYstem for Rendering Optimization</title>
		<link rel="stylesheet" type="text/css" href="css/estilos.css">
	</head>
	
	<body bgcolor="#e4dffa">

		<?php

			$handle=opendir(getcwd() . "/tmp/");
			$i=0; while ($file = readdir($handle)) {$i = $i+1;} closedir($handle);

			if(isset($_POST['submit'])) {
				
				$divisionLevel = $_POST['divisionLevel'];
				$optimizationLevel = $_POST['optimizationLevel'];	
				$nombre_archivo = $HTTP_POST_FILES['userfile']['name'];
				$tipo_archivo = $HTTP_POST_FILES['userfile']['type'];
				$tamano_archivo = $HTTP_POST_FILES['userfile']['size'];
	
				if (!((strpos($tipo_archivo, "zip")) && ($tamano_archivo < 10000000))) {
    				echo "Only .zip files and less than 15000 Kb are permitted.";
				}
				else {
					$path = "/tmp/" . $nombre_archivo;
    				if (move_uploaded_file($HTTP_POST_FILES['userfile']['tmp_name'], getcwd() . $path)) {
	  					
	  					echo "Your file was uploaded correctly.<br>";
	  					chmod(getcwd() . $path, 0777);
	  					Ice_loadProfile();
		
						try {
							$analystPrx = $ICE->stringToProxy("analyst")->ice_checkedCast("::MASYRO::Analyst");
							$workName = "work";
							$analystPrx->processWork(getcwd() . $path, $workName, $divisionLevel + 0, $optimizationLevel +0);									
						}
						catch (Ice_LocalException $ex) {
							print_r($ex);
						}
    				}
    				else {
	  					echo 'There was a problem with your Upload. Please, contact with the webmaster and tell him the problem: <a href="mailto:dvallejo.fernandez@gmail.com">David Vallejo Fernández</a>';
    				}
				} 

			} 
			else {
				echo 'Error! Please, contact with the webmaster and tell him the problem: <a href="mailto:dvallejo.fernandez@gmail.com">David Vallejo</a>';
			}
		?>

		<br>
		<center>
			<a href="visualizador.html" target="_blank">Click here to follow the process.</a>
		</center>

	</body>

</html>