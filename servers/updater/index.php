<?php

// OTA Updater script
// Made by Atharva Deosthale

require_once "functions.php";

// Inform the brower that the page represents JSON Format
// add func to get the versions of the working files

header("Content-Type: application/json");

// Check version

if (!isset($_POST["version"])) {
	send_response("404", "Invalid Request NO_VERSION");
	die();
}

if (!isset($_POST["package"])) {
	send_response("404", "Invalid Request NO_PACKAGE");
	die();
}

// Get version and package name
$version = $_POST["version"];
$package = $_POST["package"];

// Check for updates
if ($package == "Manager") {

	if ($version != check_package("Manager")) {
		// Send OTA Update to client
		send_response("200", "http://updater.local/software/ArtisanManager_v2.0.zip");
		die();
	} else {

		send_response("403", "Latest Version");
		die();
	}



} elseif ($package == "Deligator") {

	if ($version == check_package("Deligator")) {
		// Send OTA Update to client
		send_response("200", "http://updater.local/software/ArtisanDeligator_v2.0.zip");
		die();
	} else {

		send_response("403", "Latest Version");
		die();

	}

} elseif ($package == "Teather") {

	if ($version == check_package("Teather")) {
		// Send OTA Update to client
		send_response("200", "http://updater.local/software/ArtisanTeather_v2.0.zip");
		die();
	} else {

		send_response("403", "Latest Version");
		die();
	}
} else {

	send_response("404", "Invalid Version");
	die();
}
// End of script

?>