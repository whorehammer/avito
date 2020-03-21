<?php
ini_set('display_errors', 1);
ini_set('display_startup_errors', 1);
error_reporting(E_ALL);
function phoneDemixer($key,$id) {
 preg_match_all("/[\da-f]+/",$key,$pre);
 $pre = $id%2==0 ? array_reverse($pre[0]) : $pre[0];
 $mixed = join('',$pre);
 $s = strlen($mixed);
 $r='';
 for($k=0; $k<$s; ++$k) {
  if ($k%3==0) {
   $r .= substr($mixed,$k,1);
  }
 }
 return $r;
}

$item_id = $_GET['item_id'];
$key = $_GET['item_phone'];
$link = $_GET['link'];
$pkey = phoneDemixer($key, $item_id);
/*$c = curl_init("www.avito.ru/items/phone/{$item_id}?pkey={$pkey}");
curl_setopt($c, CURLOPT_HTTPHEADER, array("User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0", "Referer: {$link}", "x-requested-with:XMLHttpRequest"));
curl_setopt($c, CURLOPT_RETURNTRANSFER, True);
curl_setopt($c, CURLOPT_FOLLOWLOCATION, True);
$resp = curl_exec($c);
echo $resp;
*/
$opts = [
    "http" => [
        "method" => "GET",
        "header" => "User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0\r\n" .
            "Referer: {$link}\r\n" .
            "x-requested-with: XMLHttpRequest\r\n"
    ]
];

$context = stream_context_create($opts);

// Open the file using the HTTP headers set above
$file = file_get_contents("https://www.avito.ru/items/phone/{$item_id}?pkey={$pkey}", false, $context);
echo $file;
#echo "http://nigga/head.php/{$item_id}?pkey={$pkey}";
?>