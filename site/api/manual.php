<?php
require_once 'database.php';

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    if(isset($_POST['type'])){
        if($_POST['type'] === 'INSERT'){
            if($_POST['speed']=="NULL"){
                $sql = "INSERT INTO manual (speed) VALUES (NULL)";
            }else{
                $sql = "INSERT INTO manual (speed) VALUES ('".$_POST['speed']."')";
            }
            if ($conn->query($sql) === TRUE) {
                echo "true";
            } else {
                echo "false";
            }
        }else if($_POST['type'] === 'DELETE'){
            $sql = "delete from manual; ALTER TABLE manual AUTO_INCREMENT=1;";
            if (mysqli_multi_query($conn,$sql)) {
                echo "true";
            } else {
                echo "false";
            }
        }else if($_POST['type'] === 'RECENT'){
            $sql = "SELECT * FROM manual order by id desc limit 1;";
            $result = $conn->query($sql);
            if ($result->num_rows > 0) {
                $row =  mysqli_fetch_assoc($result);
                echo json_encode($row);
            }else{
                echo "false";
            }
        } else{
            echo "Not a valid type parameter";
        }
    }else {
        echo "Specify a type parameter";
    }
} else if ($_SERVER['REQUEST_METHOD'] === 'GET') {
    $json = [];
    $sql = "SELECT * FROM manual;";
    $result = $conn->query($sql);
    while($row = mysqli_fetch_assoc($result)){
        $json[] = $row;
    }
    echo json_encode($json);
}