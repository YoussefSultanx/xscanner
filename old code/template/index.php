<?php
//$url = 'http://localhost:5000/hello'; // Change the URL to your Flask server address
//$response = file_get_contents($url);
//echo $response;


session_start();
  include_once "../models/Classes/UserClass.php";

if(!empty($_SESSION['UserID'])) {
    $UserObject=new User($_SESSION["UserID"]);
}
else{

}
?>
<!DOCTYPE html>
<html lang="en">
<head>
<?php include 'navigation&footer/navhome.php'?>
  <title>Home</title>
  <!-- MDB icon -->


</head>
<body>
    

<!--Main Navigation-->

<header>
<!--Navbar-->


<!--/.Navbar-->
<!--Mask-->
      <div style="width: fixed;">
        <div>
    <div class="container" >

        <div class="header" style="width:fixed;">
    <h2><font size=4>Home Page</font></h2>
  </div>
  <div class="content"style="width: fixed;" >

    <?php if (isset($_SESSION['success'])): ?>
      <div class="error success">
         <h3>
            <?php
               echo $_SESSION['success'];
               unset($_SESSION['success']);
            ?>
          </h3> 
      </div>
    <?php endif ?>

<div class="row" style="inline-size: fixed" >
  <div class="column" style="margin-right: 100px">

    <img src="css/home1ed.png" alt="Snow" style="margin-left: 100px ;width:300px;height:300px">
        <h4 style="margin-left: 100px "><font color='White' size="100">Our Features</font></h4>

        <p style="margin-left: 100px ;width:330px;height:300px"> <font color="white" size="5" style="font-family: bardley hand,cursive;">X-Scanner an advanced web se-
curity tool. This tool is designed specifically to enhance the overall security of web applications, Detects SQL injections, XSS, Port Scanning and RCE threats </font> </p>
  </div>


  <div class="column" style=" margin-right: 100px; margin-top: 400px;">
    <img src="css/tools.jpg" alt="Forest"  style="width:300px;height:300px">

              <p style="margin-left: 10px ;width:330px;height:300px; max-height: fixed ;"> <font color="white" size="5" style="font-family: bardley hand,cursive;">Choose your preferred types for the scan or do a Full scan</font> </p>
  </div>
 

   <div class="column" style=" margin-right: 200px; margin-top: 500px;">
    <img src="css/dev.jpg" alt="Mountains" style="width:300px;height:300px">

              <p style="margin-left: 10px ;width:330px;height:300px; max-height: fixed ;"> <font color="white" size="5" style="font-family: bardley hand,cursive;">X-Scanner is free, fully and available for pentesters to adjust and develop the source code to meet their requirements if desired.
</font> </p>
    
  </div>
</div>
</div>
</div>
           
  </div>
</div>
<!--/.Mask-->
</header>
<!--Main Navigation-->

<!--Main layout-->
<main>

</main>
<!--Main layout-->

<!--Footer-->
<footer>
<?php include 'Navigation&footer/footer1.php'?>
</footer>

<!--Footer-->



  <!-- jQuery -->
  <script type="text/javascript" src="js/jquery.min.js"></script>
  <!-- Bootstrap tooltips -->
  <script type="text/javascript" src="js/popper.min.js"></script>
  <!-- Bootstrap core JavaScript -->
  <script type="text/javascript" src="js/bootstrap.min.js"></script>
  <!-- MDB core JavaScript -->
  <script type="text/javascript" src="js/mdb.min.js"></script>
  <!-- Your custom scripts (optional) -->
  <script type="text/javascript"></script>


</html>
