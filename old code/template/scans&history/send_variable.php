<?php
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    // Retrieve variable from AJAX request
    $variable = $_POST["myVariable"];

    // Send variable to Flask endpoint using cURL
    $url = "http://localhost:5000/receive_variable"; // Assuming Flask server is running locally
    $data = array("myVariable" => $variable);

    $ch = curl_init($url);
    curl_setopt($ch, CURLOPT_POST, true);
    curl_setopt($ch, CURLOPT_POSTFIELDS, http_build_query($data));
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    $response = curl_exec($ch);
    curl_close($ch);

    echo $response;
}
?>
