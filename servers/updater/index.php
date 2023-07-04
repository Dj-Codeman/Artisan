<?php

// Artisan OTA Server
// Made by Darrion Whitfield

require_once "functions.php";

// Inform the brower that the page represents JSON Format
header("Content-Type: application/json");

// Validating Package and Version Request
if (!isset($_POST["version"])) {
	send_response("418", "UPDATE WHAT! NO_VERSION");
	die();
}

if (!isset($_POST["package"])) {
	send_response("418", "UPDATE WHAT! NO_PACKAGE");
	die();
}

$client_version = $_POST["version"];
$package = $_POST["package"];
$server_version = check_package($package);

if ($client_version == $server_version) {

	send_response("204", "Latest Version");
	die();

} elseif ($client_version != $server_version && isset($server_version)) {
	
	// Creating link to new package
	$link = "http://updater.local/software/Artisan";
	$link .= $package;
	$link .= "_v";
	$link .= $server_version;
	$link .= ".zip";

	send_response("200", $link);
	die();
} else {

	send_response("500", "The requested resource could not be found");
	die();

}

?>