<?php
	include("settings.php");

	if(isset($_POST["masterIP"])){
		writeSetting("MASTER",$_POST["masterIP"]);
	}
	if(isset($_POST["freqAttached"])){
		writeSetting("FREQ_ATTACHED",$_POST["freqAttached"]);
	}
	if(isset($_POST["rgbLed"])){
		writeSetting("RGBLED",$_POST["rgbLed"]);
	}
	if(isset($_POST["brightness"])){
		writeSetting("BRIGHTNESS",$_POST["brightness"]);
	}

	$masterIP = readSetting("MASTER");
	$myIP = $_SERVER['SERVER_ADDR'];
	$freqAttached = readSetting("FREQ_ATTACHED");
	$rgbLed = readSetting("RGBLED");
	$brightness = readSetting("BRIGHTNESS");
?>

<form action="index.php" method="POST">
	<input type="text" name="masterIP" value="<?php echo $masterIP;?>"></input> MASTER IP ADDRESS<br>
	<input type="text" value="<?php echo $myIP;?>"></input> SLAVE IP ADDRESS<br>
	<input type="text" name="freqAttached" value="<?php echo $freqAttached;?>"></input> FREQUENCY ATTATCHED<br>
	<select name="rgbLed">
		<option value="ENABLED">ENABLED</option>
		<option value="DISABLED">DISABLED</option>
	</select> RGB LED<br>
	<input type="text" name="brightness" value="<?php echo $brightness;?>"></input> LED BRIGHTNESS<br><br><br>
	<input type="submit" value="UPDATE"></input>
</form>
