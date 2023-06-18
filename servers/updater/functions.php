<?php

// OTA Update Script
// Made by Atharva Deosthale

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
	$manager_path = "/root/Artisan-Hosting/Machine-Management/client";
	$deligator_path = "/root/Artisan-Hosting/Machine-Management/server";
	$teather_path = "/root/Artisan-Hosting/Machine-Management/teather";

	if($name == "Manager") {
		// do somthing to get the latest version
		$version_path = $manager_path .= "/version.ar";
		$version = file_get_contents($version_path);
	} elseif($name == "Deligator") {
		$version_path = $deligator_path .= "/version.ar";
		$version = file_get_contents($version_path);
	} elseif($name == "Teather") {
		$version_path = $teather_path .= "/version.ar";
		$version = file_get_contents($version_path);
	} else {
		die("Sir this is wendys");
	}

	return $version;
}
?>
