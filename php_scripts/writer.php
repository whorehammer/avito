<?php
$string = "{$_GET['title']}#{$_GET['date']}#{$_GET['name']}#{$_GET['phone']}#{$_GET['href']}\n\n";
file_put_contents("log.txt", $string, FILE_APPEND | LOCK_EX);
?>