<?php
 include 'AdminNav.php';


  if(empty($_SESSION['UserID'])) {

         header('location: ../../index.php');
        }
        else{
      $Accept=$_GET['id'];
      xscan::AdmindeleteScan($Accept);
      header('location: admin_panel_scans.php');
    }

?>