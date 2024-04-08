<?php


include "DB.php";


//X-SCANNER xport TABLE
class xports {
	public $id;
	public $port;
	public $scanID;
	//

	//public $options;
	function __construct($id) {
		//$db_handle = new DB();
		$sql="SELECT * FROM xports WHERE id=".$id;
		$result12 = mysqli_query($GLOBALS['con'],$sql);
		if($row12=mysqli_fetch_array($result12)){
			$this->id=$row12['ID'];
			$this->port=$row12['portID'];
			$this->scanID=$row12['scanID'];


	
		}
		else {

			$this->id="";
			$this->port="";
			$this->scanID="";
		}
	}

	static function portscan($ID)	{
		$products=[];
		$i=0;
		
		$sql="SELECT * from xports WHERE scanID =".$ID;
		$result = mysqli_query($GLOBALS['con'],$sql);
		
		while($row=mysqli_fetch_array($result)){
			$products[$i++]=new xports($row[0]);
		}
		return $products;
		
		}

	
	
}
// scans TABLE
class xscan {
	public $id;
	public $userID;
	public $xscanID;
	//

	//public $options;
	function __construct($id) {
		//$db_handle = new DB();
		$sql="SELECT * FROM scans WHERE id=".$id;
		$result123 = mysqli_query($GLOBALS['con'],$sql);
		if($row123=mysqli_fetch_array($result123)){
			$this->id=$row123['ID'];
			$this->userID=$row123['userID'];
			$this->xscanID=$row123['ScanID'];


	
		}
		else {

			$this->id="";
			$this->userID="";
			$this->xscanID="";
		}
	}

	static function getmyScans($UID)	{
		$products=[];
		$i=0;
		
		$sql="SELECT * from scans WHERE userID ='$UID'";
		$result = mysqli_query($GLOBALS['con'],$sql);
		
		while($row=mysqli_fetch_array($result)){
			$products[$i++]=new xscan($row[0]);
		}
		return $products;
		
		}

		static function getallscans()	{
			$products=[];
			$i=0;
			
			$sql="SELECT * from scans ";
			$result = mysqli_query($GLOBALS['con'],$sql);
			
			while($row=mysqli_fetch_array($result)){
				$products[$i++]=new xscan($row[0]);
			}
			return $products;
			
			}

			static function AdmindeleteScan($ObjUser){
			
				$sql= "DELETE FROM scans WHERE ScanID =".$ObjUser;
				$result=mysqli_query($GLOBALS['con'],$sql);
						if(mysqli_query($GLOBALS['con'],$sql)){
				
						
					return true;}
				else
					return false;
				
			}			
	
	
}

// XSS TABBLE
class xss {
	public $id;
	public $xssresult;
	public $scanID;
	//

	//public $options;
	function __construct($id) {
		//$db_handle = new DB();
		$sql="SELECT * FROM xss WHERE id=".$id;
		$result12 = mysqli_query($GLOBALS['con'],$sql);
		if($row12=mysqli_fetch_array($result12)){
			$this->id=$row12['ID'];
			$this->xssresult=$row12['xssresult'];
			$this->scanID=$row12['scanID'];


	
		}
		else {

			$this->id="";
			$this->xssresult="";
			$this->scanID="";
		}
	}

	static function xss_scan($ID)	{
		$products=[];
		$i=0;
		
		$sql="SELECT * from xss WHERE scanID =".$ID;
		$result = mysqli_query($GLOBALS['con'],$sql);
		
		while($row=mysqli_fetch_array($result)){
			$products[$i++]=new xss($row[0]);
		}
		return $products;
		
		}

	
	
}

// SQL TABBLE
class xsql {
	public $id;
	public $xsql;
	public $scanID;
	//

	//public $options;
	function __construct($id) {
		//$db_handle = new DB();
		$sql="SELECT * FROM xsql WHERE id=".$id;
		$result12 = mysqli_query($GLOBALS['con'],$sql);
		if($row12=mysqli_fetch_array($result12)){
			$this->id=$row12['ID'];
			$this->xsql=$row12['sqlresult'];
			$this->scanID=$row12['scanID'];


	
		}
		else {

			$this->id="";
			$this->xsql="";
			$this->scanID="";
		}
	}

	static function xsql_scan($ID)	{
		$products=[];
		$i=0;
		
		$sql="SELECT * from xsql WHERE scanID =".$ID;
		$result = mysqli_query($GLOBALS['con'],$sql);
		
		while($row=mysqli_fetch_array($result)){
			$products[$i++]=new xsql($row[0]);
		}
		return $products;
		
		}

	
	
}




?>