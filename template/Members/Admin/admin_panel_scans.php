
<!DOCTYPE html>
<html lang="en">
<head>
<?php include 'AdminNav.php'?>
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
 <th ><p style="color:White">User ID</th>
 <th><p style="color:White">Scan ID</th>
 <th><p style="color:White">Delete User</th>

  <?php 
$allProducts=xscan::getallscans();
  foreach ($allProducts as $product){?>
  
     
        
          <tr>

           <td><p style="color:White"><?php echo $product->userID ?></td>
            <td><p style="color:White"><?php echo $product->xscanID ?></td>
                <td><input type="submit" name="addto" value="Remove" class="btnAddAction" onclick="location.href='admin_delete_scan.php?action=add&id=<?php echo $product->xscanID ?>'" /></td>

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
