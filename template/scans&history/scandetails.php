
<!DOCTYPE html>
<html lang="en">
<head>
<?php 
session_start();
  include_once "../../models/Classes/productsClasses.php";
include '../Navigation&footer/scandetailsnav.php'
?>
  
  <title>Users List</title>

</head>
<body>
<!--Main Navigation-->
<header>
<!--Navbar-->


<!--/.Navbar-->
<!--Mask-->
  <div class="header">
  
  
  
 
  
  


<table class="table " style="background: rgba(34, 38, 43);">
 <th ><p style="color:White">Scan id</th>
 <th><p style="color:White">XSS report</th>

  <?php
  $product_name=$_GET['id'];
 // echo '<script>alert("' . $product_name . '")</script>';
  $portsss=xports::portscan($product_name);
  foreach ($portsss as $port){?>
  
     
        
          <tr>

           <td><p style="color:White"><?php echo $port->scanID?></td>
            <td><p style="color:White"><?php echo $port->port ?></td>

                </tr>
    
      
        <div>
          
          
        
        
      </form>
    </div>
    <?php
  }
  ?>
</table>


<table class="table " style="background: rgba(34, 38, 43);">
 <th ><p style="color:White">Scan id</th>
 <th><p style="color:White">SQL report</th>

  <?php

  $portsss=xsql::xsql_scan($product_name);
  foreach ($portsss as $port){?>
  
     
        
          <tr>

           <td><p style="color:White"><?php echo $port->scanID?></td>
            <td><p style="color:White"><?php echo $port->xsql ?></td>

                </tr>
    
      
        <div>
          
          
        
        
      </form>
    </div>
    <?php
  }
  ?>
</table>

<table class="table " style="background: rgba(34, 38, 43);">
 <th ><p style="color:White">Scan id</th>
 <th><p style="color:White">XSS Report</th>

  <?php
  $product_name=$_GET['id'];
 // echo '<script>alert("' . $product_name . '")</script>';
  $portsss=xss::xss_scan($product_name);
  foreach ($portsss as $port){?>
  
     
        
          <tr>

           <td><p style="color:White"><?php echo $port->scanID?></td>
            <td><p style="color:White">Port: <?php echo $port->xssresult ?></td>

                </tr>
    
      
        <div>
          
          
        
        
      </form>
    </div>
    <?php
  }
  ?>

</table>


<!--/.Mask-->
</header>
<!--Main Navigation-->

<!--Main layout-->
<main>

</main>
<!--Main layout-->

<!--Footer-->
<footer>

</footer>

<!--Footer-->



  <!-- jQuery -->
<?php include '../../Navigation&footer/navscript.php'?>

</body>
</html>