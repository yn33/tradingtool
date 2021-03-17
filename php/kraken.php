#!/usr/bin/php
<?php

require_once 'KrakenAPIClient.php'; 
require_once 'functions.php';

$keyfile = fopen("keys.txt", "r");
$key = str_replace("\n", '', fgets($keyfile));
$secret = str_replace("\n", '', fgets($keyfile));
fclose($keyfile);

$url = 'https://api.kraken.com';
$sslverify = $url ? false : true;
$version = 0;

$kraken = new Payward\KrakenAPI($key, $secret, $url, $version, $sslverify);
$interval = 0;
$assetPair = "";
$enter = false;
$goal = false;

foreach($argv as $arg) {
    if($arg != "C:/kraken-api-client-master/php/kraken.php") {
        if($arg == "balance") {
            balance();
        } else if($arg == "openorders") {
            openOrders();
        } else if($arg == "tradebalance") {
            tradeBalance();
        } else if($arg == "link") {
            $assetPair = 'LINKEUR';
        } else if($arg == "xbt") {
            $assetPair = 'XXBTZEUR';
        } else if($arg == "eth") {
            $assetPair = 'XETHZEUR';
        } else if($arg == "xrp") {
            $assetPair = 'XXRPZEUR';
        } else if($arg == "ltc") {
            $assetPair = 'XLTCZEUR';
        } else if($arg == '15' || $arg == '5' || $arg == '1' || $arg == '30' || $arg == '60') {
            $interval = $arg;
        } else if($arg == 'enter') {
            $enter = true;
            break;
        } else if($arg == 'goal') {
            $goal = true;
            break;
        } else if($arg == "clear") {
            clear();
        }
    }
}

if($interval != 0 && $assetPair != "") {
    getOHLC($assetPair, $interval);
} else if($enter && $assetPair != "") {
    $curr = $argv[len($argv) - 3];
    if($curr == 'enter') {
        $stop = floatval($argv[i + 1]);
        $buyVolume = floatval($argv[i + 2]);
        entry($assetPair, $stop, $buyVolume);
    }
} else if($goal && $assetPair != "") {
    $curr = $argv[len($argv) - 3];
    if($curr == 'goal') {
        $stop = floatval($argv[i + 1]);
        $sellVolume = floatval($argv[i + 2]);
        raiseStop($assetPair, $stop, $sellVolume);
    }
}
?>
