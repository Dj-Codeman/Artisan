<?php

// OTA Update Script
// Made by Atharva Deosthale

// Set cURL URL (master server address) and may not be localhost
$url = "http://updater.local/index.php";
$package = "Manager"; // deploy diffrent servers with this set
$version = shell_exec("artisan --version-cli");

// set POST data
$data = [
    "version" => $version,
    "package" => $package
];

if (is_dir("/tmp/artisan_update")){
    rmdir("/tmp/artisan_update");
}

if (is_dir("/tmp/artisan_fallback")){
    rmdir("/tmp/artisan_fallback");
}
// Create HTTP POST Data
$datastring = http_build_query($data);

// open connection
$connection = curl_init($url);

// set cURL options in an array 

$options = array(
    CURLOPT_POST => true,
    CURLOPT_POSTFIELDS => $datastring,
    CURLOPT_RETURNTRANSFER => true,
);

// establish connection and execute instruction and capture the response
curl_setopt_array($connection, $options);

// getting the data back 
$response = curl_exec($connection);

// phrasing the response 
$data = json_decode($response, true); //true bool returns data as an array

#! check for status code status message
if ($data["status_code"] == "200") {
    // save link
    $link = $data["status_message"];

} elseif ($data["status_code"] == "404") {
    // kill app 
    die("You have requested and invalid package \n");

} else {
    die("You have the latest version \n");
}

// Start update
echo "New version found! " ."\n". "Updating Artisan Suite...." ."\n";

// Download update package
file_put_contents("/tmp/update.zip", file_get_contents($data["status_message"]));

// Get project path

// Zip file name
$filename = '/tmp/update.zip';
$zip = new ZipArchive;
$res = $zip->open($filename);
if ($res === TRUE) {

 // Unzip path
 $path = "/tmp/artisan_update/";

 // Extract file
 $zip->extractTo($path);
 $zip->close();

 echo 'Unpacked\nInstalling...';
} else {
 echo 'failed!';
 die("An error occoured while downloading the update");
}

// start update process
shell_exec("bash /tmp/artisan_update/updater/update.sh"); // * this is what applies the new updates and fixes the daemons
die();

?>