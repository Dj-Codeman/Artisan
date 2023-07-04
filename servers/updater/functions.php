<?php

// Artisan OTA Server
// Made by Darrion Whitfield

// Function to send response to the client in the JSON Format

function send_response($x,$y) {
	// Create response in form of array
	$response["status_code"] = $x;
	$response["status_message"] = $y;

	// Encode the data into JSON Format
	$json = json_encode($response);
	// RESPOND
	echo $json;
	die();
}

function check_package($name) {
	$manager_path = "/opt/Artisan/client";
	// update the paths
	$deligator_path = "/opt/Artisan/server";
	$teather_path = "/opt/Artisan/teather";

	if($name == "Manager") {
		$version_path = $manager_path .= "/version.ar";
		$version = file_get_contents($version_path);

	} elseif($name == "Deligator") {
		$version_path = $deligator_path .= "/version.ar";
		$version = file_get_contents($version_path);

	} elseif($name == "Teather") {
		$version_path = $teather_path .= "/version.ar";
		$version = file_get_contents($version_path);

	} else {

		send_response("500", "Internal Server Error");

	}

	return $version;
}
?>
