<?php
require_once 'database.php';

function getAutoSetting($id){
    global $conn;
    $sql = "SELECT * FROM auto where id=".$id.";";
    $result = $conn->query($sql);
    if ($result->num_rows > 0) {
        $row =  mysqli_fetch_assoc($result);
        return $row;
    }else{
        return -1;
    }
}

function getManualSetting($id){
    global $conn;
    $sql = "SELECT * FROM manual where id=".$id.";";
    $result = $conn->query($sql);
    if ($result->num_rows > 0) {
        $row =  mysqli_fetch_assoc($result);
        return $row;
    }else{
        return -1;
    }
}

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    if(isset($_POST['type'])){
        if($_POST['type'] === 'INSERT'){
            if( isset($_POST['auto_id']) ){
                $sql = "INSERT INTO data (humidity, temperature, auto_id) VALUES ('".$_POST['humidity']."', '".$_POST['temperature']."', '".$_POST['auto_id']."')";
            }else{
                $sql = "INSERT INTO data (humidity, temperature, manual_id) VALUES ('".$_POST['humidity']."', '".$_POST['temperature']."', '".$_POST['manual_id']."')";
            }
            if ($conn->query($sql) === TRUE) {
                echo "true";
            } else {
                echo "false";
            }
        }else if($_POST['type'] === 'DELETE'){
            $sql = "TRUNCATE TABLE data";
            if ($conn->query($sql) === TRUE) {
                echo "true";
            } else {
                echo "false";
            }
        }else{
            echo "Not a valid type parameter";
        }
    }else{
        echo "Specify a type parameter";
    }
} else if ($_SERVER['REQUEST_METHOD'] === 'GET') {
    $json = [];
    $sql = "SELECT * FROM data;";
    $result = $conn->query($sql);
    while($row = mysqli_fetch_assoc($result)){
        if(!is_null($row['auto_id'])){
            $id = $row['auto_id'];
            $setting = getAutoSetting($id);
            unset($row->auto_id);
            unset($row->manual_id);
            $row['auto'] = (object) $setting;
        }else{
            if(!is_null($row['manual_id'])){
                $id = $row['manual_id'];
                $manual = getManualSetting($id);
                unset($row->auto_id);
                unset($row->manual_id);
                $row['manual'] = (object) $manual;
            }else{
                unset($row->auto_id);
                unset($row->manual_id);
            }    
        }
        $json[] = $row;
    }
    echo json_encode($json);
}