#!/usr/bin/php
<?php

print_r("Starting.\n"); 

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
$assetPairs = array();

clearstatcache();

foreach($argv as $arg) {
    if($arg != "tradebot.php") {
        if($arg == "trade_testmode") {
            $TEST_MODE = true;
            print_r("Trading in test mode.");
            print_r("\n");
            if(filesize("data.txt") > 1) {
                processTrade();
            } else {
                scan();
            }
        } else if($arg == "trade") {
            $TEST_MODE = false;
            $SCAN = false;
            print_r("Trading without test mode.");
            print_r("\n");
            if(filesize("data.txt") > 1) {
                processTrade();
            } else {
                scan();
            }
        } else if($arg == "scan") {
            $TEST_MODE = false;
            $SCAN = true;
            print_r("Scanning only.");
            print_r("\n");
            if(filesize("data.txt") > 1) {
                processTrade();
            } else {
                scan();
            }
        } else if($arg == "balance") {
            balance();
        } else if($arg == "openorders") {
            openOrders();
        } else if($arg == "tradebalance") {
            tradeBalance();
        } else if($arg == "link") {
            array_push($assetPairs, 'LINKEUR');
        } else if($arg == "xbt") {
            array_push($assetPairs, 'XXBTZEUR');
        } else if($arg == "eth") {
            array_push($assetPairs, 'XETHZEUR');
        } else if($arg == "xrp") {
            array_push($assetPairs, 'XXRPZEUR');
        } else if($arg == "ltc") {
            array_push($assetPairs, 'XLTCZEUR');
        } else if($arg == "clear") {
            clear();
        } else {
            print_r("Incorrect syntax.");
            print_r("\n");
        }
    }
}

?>
