<?php
require_once("../../models/Classes/productsClasses.php");
session_start();
if(empty($_SESSION['UserID'])) 
{
  header('location: ../index.php');
} 
?>
	<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
  <meta http-equiv="x-ua-compatible" content="ie=edge">
  <title>Scan History</title>
  <!-- MDB icon -->
   <link rel="icon" href="../img/products.ico" type="image/x-icon">
  <!-- Font Awesome -->
  <link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.11.2/css/all.css">
  <!-- Google Fonts Roboto -->
  <link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Roboto:300,400,500,700&display=swap">
  <!-- Bootstrap core CSS -->
  <link rel="stylesheet" href="../css/bootstrap.min.css">
  <!-- Material Design Bootstrap -->
  <link rel="stylesheet" href="../css/mdb.min.css">
  <!-- Your custom styles (optional) -->
    <link rel="stylesheet" href="../css/StyleProducts.css">
<link href="../css/stprod.css" type="text/css" rel="stylesheet" />
</head>
<body>
	<!--Main Navigation-->
<header>
<!--Navbar-->
<?php include '../Navigation&footer/NavProd.php'?>

<!--/.Navbar-->
<!--Mask-->


</div>

  <div class="content" >

  <div id="product-grid">
	<div class="txt-heading" id="q157"><h3>Scan History</h2></div>
	<?php	

	$allProducts=xscan::getmyScans($_SESSION['UserID']);
  
	foreach ($allProducts as $product){?>
		<div class="product-item" width="200px" id="q157">
    <form method="post" action="scandetails.php?id=<?php echo $product->xscanID;?>">
				<div><strong>Scan ID: <?php echo $product->xscanID; ?></strong></div>
        <?php $sqlscan=xsql::xsql_scan($product->xscanID); ?>
        <?php $portsss=xports::portscan($product->xscanID); ?>
        <?php $xssscan=xss::xss_scan($product->xscanID); ?>
        <!-- <?php $rcescan=xsql::xsql_scan($product->xscanID); ?> -->
        <!--<div><strong>TEST ID: <?php print_r($portsss) ?></strong></div> -->

				
<!-- 				
        <div style="white-space:nowrap">
                            
                            <h6 class="text-secondary"><i>XSS: </i><?php echo $product->xscanID; ?></h6>
                            <h6 class="text-secondary"><i>Port Scan: </i><?php echo $product->xscanID; ?></h6>
                            <h6 class="text-secondary"><i>RCE: </i><?php echo $product->xscanID; ?></h6>
                            <h6 class="text-secondary"><i>SQL: </i><?php echo $product->xscanID; ?></h6>
                            <h6 class="text-secondary"><i>Status: </i>Scan Completed</h6>
                            </div>
                            <div> -->

				
        <div style="white-space:nowrap">
                            <?php if(empty($portsss))
                            {?>

                              <h6 class="text-secondary"><i>Port Scan: </i> Not Detected</h6>
                            <?php 
                            }
                            else{  
                                  ?>
                            <h6 class="text-secondary"><i>Port Scan: </i>Detected</h6> <?php 
                              } ?>



                            <?php if(empty($xssscan))
                            {?>

                              <h6 class="text-secondary"><i>XSS: </i> Not Detected</h6>
                            <?php 
                            }
                            else{  
                                  ?>
                            <h6 class="text-secondary"><i>XSS: </i>Found vulnerability</h6> <?php 
                              } ?>

                            <?php if(empty($sqlscan))
                            {?>

                              <h6 class="text-secondary"><i>SQL: </i> No vulnerability</h6>
                            <?php 
                            }
                            else{  
                                  ?>
                            <h6 class="text-secondary"><i>SQL: </i>Found vulnerability</h6> <?php 
                              } ?>




                            <h6 class="text-secondary"><i>RCE: </i>No vulnerability</h6>
                            <h6 class="text-secondary"><i>Status: </i>Scan Completed</h6>
                            </div>
                            <div>
                            
          
          <input type="submit" name="addto" value="Scan Details" class="btnAddAction" />
        </div>
                
			
				<div>
					
				
				</div>
			
			</form>
		</div>
		<?php
	}
	?>
</content>

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

</footer>

<!--Footer-->



  <!-- jQuery -->
<?php include '../Navigation&footer/navscript2.php'?>


</div>
</header>
</body>
</html>
