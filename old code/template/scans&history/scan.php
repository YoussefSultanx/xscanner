
<?php 
session_start();
  include_once "../../models/Classes/UserClass.php";
include '../Navigation&footer/Navscan.php';

if(isset($_POST['submit'])){
  include_once "../../models/Classes/UserClass.php";

    // $scanID=$_POST['FName'];

  
    //   echo $scanID . "<br>";
    //   echo '<script>alert("' . $scanID . '")</script>';

  
  // $UserName=$_POST['methods'];
//   sleep(5);
//   echo "<SCRIPT> ";
      

//   echo  " window.location.replace('../../index.php');
// </SCRIPT>";
 
  // foreach($UserName as $item)
  // {
  //     echo $item . "<br>";
  //     echo '<script>alert("' . $item . '")</script>';

  // }
  // $url = 'http://localhost:5000/hello'; // Change the URL to your Flask server address
  // $response = file_get_contents($url);
  // echo $response;

}
?>
  
<!DOCTYPE html>
<html lang="en">
<head>

  <title>Login</title>

</head>
<body>

<!--Main Navigation-->
<header>
<!--Navbar-->

<!--/.Navbar-->

<!--Mask-->
  <div class="header">

    <h2><font size=4>Scan</font></h2>
  </div>
  <form action="http://localhost:5000/receive_data" method="post">


  
 <!-- <?php


?> -->
  
  <div class="input-group">
<i class="fa fa-search"></i>
    <label><font color="white">Enter URL Target</font></label>
    <input type="text" placeholder="Target URL without 'https//' " name="url" required="">
    
    </div>
    <?php
    $random_number = rand(100, 999); 
    echo "<input type='hidden' id='ScanID' name='ScanID' required value=".$random_number.'>';
    echo "<input type='hidden' id='userconID' name='userconID' required value=".$UserObject->ID.'>'
    ?>

    
 
  <div class="input-group">
    <i class="fa fa-check"></i>
    <br>
        <label><font color="white">Choose what to scan for !</font></label> </div>

        <style>
  /* Custom checkbox styles */
  .custom-checkbox input[type="checkbox"] {
    width: 1.25rem;
    height: 1.25rem;
  }
  .custom-checkbox input[type="checkbox"]:checked + .checkmark {
    background-color: #007bff;
    border-color: #007bff;
  }
  .custom-checkbox input[type="checkbox"]:checked + .checkmark:after {
    display: block;
  }
  .custom-checkbox .checkmark:after {
    content: "";
    position: absolute;
    display: none;
    left: 5px;
    top: 2px;
    width: 5px;
    height: 10px;
    border: solid white;
    border-width: 0 2px 2px 0;
    transform: rotate(45deg);
  }
</style>

        <div class="custom-checkbox form-check" style="display: flex;">
        
    <input type="checkbox" name="methods[]" value="XSS" style=" margin-right: 10px" > <font color="white">XSS</font>&ensp;&ensp;&ensp;&ensp;&ensp;  
    <input type="checkbox" name="methods[]" value="SQL" style=" margin-right: 10px"> <font color="white">SQL</font> &ensp;&ensp;&ensp;&ensp;&ensp; 
    <input type="checkbox" name="methods[]" value="PortScan" style=" margin-right: 10px"> <font color="white">Port Scanning</font>&ensp;&ensp;&ensp;&ensp;&ensp; 
    <input type="checkbox" name="methods[]" value="RCE" style=" margin-right: 10px"> <font color="white">RCE</font> &ensp;&ensp;&ensp;&ensp;&ensp; 




</div>

  <div class="input-group">
    <button type="sumbit" name="submit" class="btn" style="margin-left: 230px " >Start Scan!</button>

  </div>

 </form>
<!--/.Mask-->
</header>
<!--Main Navigation-->

<!--Main layout-->
<main>

</main>
<!--Main layout-->

<!--Footer-->
<footer>
<?php include '../Navigation&footer/footer2.php'?>
</footer>
<!--Footer-->



  <!-- jQuery -->
<?php include '../Navigation&footer/navscript.php'?>
<!-- <script>
function sendVariable() {
    var variable = document.getElementById("fch").value;

    // AJAX request to PHP endpoint
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "send_variable.php", true);
    xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
    xhr.onreadystatechange = function() {
        if (xhr.readyState === 4 && xhr.status === 200) {
            console.log(xhr.responseText);
        }
    };
    xhr.send("myVariable=" + variable);
}
</script> -->
</body>
</html>