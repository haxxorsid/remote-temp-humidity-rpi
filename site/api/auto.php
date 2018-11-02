<?php
require_once 'database.php';

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    if(isset($_POST['type'])){
        if($_POST['type'] === 'INSERT'){
            $sql = "INSERT INTO auto (lowh, mediumh, highh, lowt, mediumt, hight) VALUES ('".$_POST['lowh']."', '".$_POST['mediumh']."', '".$_POST['highh']."', '".$_POST['lowt']."', '".$_POST['mediumt']."', '".$_POST['hight']."')";
            if ($conn->query($sql) === TRUE) {
                echo "true";
            } else {
                echo "false";
            }
        }else if($_POST['type'] === 'DELETE'){
            $sql = "DELETE FROM auto WHERE id NOT IN ( SELECT id FROM ( SELECT id FROM auto ORDER BY id DESC LIMIT 1 ) foo );";
            if ($conn->query($sql) === TRUE) {
                echo "true";
            } else {
                echo "false";
            }
        }else if($_POST['type'] === 'RECENT'){
            $sql = "SELECT * FROM auto order by id desc limit 1;";
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
    $sql = "SELECT * FROM auto;";
    $result = $conn->query($sql);
    while($row = mysqli_fetch_assoc($result)){
        $json[] = $row;
    }
    echo json_encode($json);
}