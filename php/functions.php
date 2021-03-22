<?php

function getOHLC($assetPair, $interval) {

    global $kraken;
    $res = $kraken->QueryPublic('OHLC', array('pair' => $assetPair, 'interval' => $interval));
    $res1 = $res['result'][$assetPair];
    fwrite(STDOUT, json_encode($res1));
}

function scan() {

    global $TEST_MODE;
    global $kraken;
    global $assetPairs;
    global $SCAN;

    if($TEST_MODE) {
        print_r("Scanning in test mode.");
        print_r("\n");
    } else {
        print_r("Scanning without test mode.");
        print_r("\n");
    }
    if(!$SCAN) {
        print_r("Entering on.");
        print_r("\n");
    } else {
        print_r("Entering off.");
        print_r("\n");
    }

    $VOLUME_LEVEL = 2.0;
    $CHANGE_LEVEL = 2.0;
    $SCORE_LEVEL = 8.0;
    $AMOUNT_OF_BARS = 6.0;
    $CHUNK_SIZE = 10;
    $PIVOT_LEVEL = 1.0;
    $PIVOT_DIST_BAR_LENGTHS = 1.0;
    $CHANGE_SCALE = 2.0;
    $VOLUME_SCALE = 2.0;
    $SUPPORT_SCALE = 1.0;
    $RESISTANCE_SCALE = 1.0;
    $STOP = 0.3;
    $COST = 36;
    $COST_LOW = 31;

    foreach($assetPairs as $assetPair) {
        
        $interval = 15;
        $res = $kraken->QueryPublic('OHLC', array('pair' => $assetPair, 'interval' => $interval));
        $res1 = $res['result'][$assetPair];
        $chunks = array_chunk($res1, $CHUNK_SIZE);
        $supports = array_map('findLow', $chunks);
        $resistances = array_map('findHigh', $chunks);
        array_pop($supports);
        array_pop($resistances);

        $count = 0;
        $volumeTotal = 0;
        $changeTotal = 0;

        foreach($res1 as $bar) {
            $time = $bar[0];
            $open = $bar[1];
            $high = $bar[2];
            $low = $bar[3];
            $close = $bar[4];
            $volume = $bar[6];
            $volumeTotal = $volumeTotal + $volume;
            if($open >= $close) {
                $changeTotal = $changeTotal + ($open - $close);
            } else {
                $changeTotal = $changeTotal + ($close - $open);
            }        
            $count += 1;
        }

        $volumeAvg = $volumeTotal / $count;
        $changeAvg = $changeTotal / $count;
        $volumeLevel = $volumeAvg*$VOLUME_LEVEL;
        $changeLevel = $changeAvg*$CHANGE_LEVEL;

        $lastBar = $res1[count($res1)-2];
        $lastBarTime = $lastBar[0];
        $lastBarChange = $lastBar[4] - $lastBar[1];
        print_r($assetPair);
        print_r("\n");
        print_r("Interval: ");
        print_r($interval);
        print_r("\n");
        print_r("Average change: ");
        print_r($changeAvg);
        print_r("\n");
        print_r("Last bar change: ");
        print_r($lastBarChange);
        print_r("\n");
        if($lastBarChange < $changeAvg) {
            $i = 2;
            $score = 0;
            $barScore = 0;
            $volumeW = 0;
            $changeW = 0;
            $supportW = 0;
            $resistanceW = 0;

            while($i < ($AMOUNT_OF_BARS + 2)) {
                $currentBar = $res1[count($res1)-$i];
                if(($currentBar[1] - $currentBar[4]) > $changeLevel) {
                    $score += 1*$CHANGE_SCALE;
                    $barScore += 1*$CHANGE_SCALE;
                    $changeW += 1;
                }
                if($currentBar[6] > $volumeLevel && $currentBar[1] > $currentBar[4]) {
                    $score += 1*$VOLUME_SCALE;
                    $barScore += 1*$VOLUME_SCALE;
                    $volumeW += 1;
                }
                $i += 1;
            }
            $stop = end($res1)[3];
            if($lastBar[3] < $stop) {
                $stop = $lastBar[3];
            }
            $entry = end($res1)[4];
            $trigger = end($res1)[1];
            $risk = $entry - $stop;
            
            $supportW = countPivots($supports, $stop, $changeAvg*$PIVOT_DIST_BAR_LENGTHS);
            $score += $supportW*$SUPPORT_SCALE;

            $resistanceW = countPivots($resistances, $stop, $changeAvg*$PIVOT_DIST_BAR_LENGTHS);
            $score += $resistanceW*$RESISTANCE_SCALE;
            
            print_r("Change bars: ");
            print_r($changeW);
            print_R("\n");
            print_r("Volume bars: ");
            print_r($volumeW);
            print_R("\n");
            print_r("Supports: ");
            print_r($supportW);
            print_R("\n");
            print_r("Resistances: ");
            print_r($resistanceW);
            print_R("\n");

            if($entry >= $trigger && $risk > 0 && $score >= $SCORE_LEVEL && $barScore >= $SCORE_LEVEL/2) {
                $buyVolume = $STOP/$risk;
                print_r("Cost: ");
                print_r($entry*$buyVolume);
                print_r("\n");
                if($entry*$buyVolume <= $COST && $entry*$buyVolume >= $COST_LOW) {
                    $txid = array();
                    if(!$TEST_MODE && !$SCAN) {
                        $orders = $kraken->QueryPrivate('OpenOrders', array('trades' => true));
                        $ordersArray = $orders['result']['open'];
                        if(count($ordersArray) == 0) {
                            print_r($buyVolume);
                            print_r("\n");
                            /*$balance = $kraken->QueryPrivate('Balance');
                            $eur = $balance['result']["ZEUR"];*/
                            /*if($assetPair == 'XXBTZEUR' || $assetPair == 'XETHZEUR') {
                                $entry = round($entry, 1, PHP_ROUND_HALF_DOWN);
                            } else if($assetPair == 'XLTCZEUR') {
                                $entry = round($entry, 2, PHP_ROUND_HALF_DOWN);
                            } else if($assetPair == 'XXRPZEUR') {
                                $entry = round($entry, 5, PHP_ROUND_HALF_DOWN);
                            }*/
                            $order = $kraken->QueryPrivate('AddOrder', array(
                                'pair' => $assetPair, 
                                'type' => 'buy', 
                                'ordertype' => 'market', 
                                'volume' => $buyVolume,
                                'close[ordertype]' => 'stop-loss',
                                'close[price]' => $stop
                            ));
                            $error = $order['error'];
                            if(count($error) > 0) {
                                foreach($error as $err) {
                                    $recordError = fopen("log.txt", "a+");
                                    fwrite($recordError, $err);
                                    fwrite($recordError, "\n");
                                    fclose($recordError);
                                    print_r($err);
                                    print_r("\n");
                                }
                            } else {
                                print_r($order['result']['descr']['order']);
                                print_r("\n");
                                print_r($order['result']['descr']['close']);
                                print_r("\n");
                                $txid = $order['result']['txid'];
                            }
                        }
                    }
                    if(count($txid) > 0 || $TEST_MODE) {
                        $oneR = $entry - $stop;
                        $goal = $entry + 2*$oneR;
                        $datafile_1 = fopen("data.txt", "w");
                        fwrite($datafile_1, $assetPair);
                        fwrite($datafile_1, "\n");
                        fwrite($datafile_1, $lastBar[0]);
                        fwrite($datafile_1, "\n");
                        print_r("Enter: ");
                        print_r($entry);
                        fwrite($datafile_1, $entry);
                        print_r("\n");
                        fwrite($datafile_1, "\n");
                        print_r("Stop: ");
                        print_r($stop);
                        fwrite($datafile_1, $stop);
                        print_r("\n");
                        fwrite($datafile_1, "\n");
                        print_r("Goal: ");
                        print_r($goal);
                        fwrite($datafile_1, $goal);
                        print_r("\n");
                        fwrite($datafile_1, "\n");
                        fwrite($datafile_1, $oneR);
                        fwrite($datafile_1, "\n");
                        if(!$TEST_MODE) {
                            /*foreach($txid as $currtxid) {
                                fwrite($datafile_1, $currtxid);
                                fwrite($datafile_1, " ");
                            }*/
                            fwrite($datafile_1, $buyVolume);
                            fwrite($datafile_1, "\n");
                        }
    
                        $formatted = sprintf("%g %g %g %g %d %g %g %g %g %g %g %g %g %g %g", 
                        $VOLUME_LEVEL, $CHANGE_LEVEL, $SCORE_LEVEL, $AMOUNT_OF_BARS, $CHUNK_SIZE,
                        $PIVOT_LEVEL, $PIVOT_DIST_BAR_LENGTHS, $CHANGE_SCALE, $VOLUME_SCALE, $SUPPORT_SCALE, $RESISTANCE_SCALE, $volumeW, $changeW, $supportW, $resistanceW);
                        fwrite($datafile_1, $formatted);
                        fwrite($datafile_1, "\n");
                        fclose($datafile_1);    
                    }
                }
            }
        }
    }
}

function processTrade() {

    global $TEST_MODE;
    global $kraken;

    if($TEST_MODE) {
        print_r("Processing trade in test mode.");
        print_r("\n");
    } else {
        print_r("Prosessing trade without test mode.");
        print_r("\n");
    }
    $datafile_2 = fopen("data.txt", "r");
    $assetPair = str_replace("\n", '', fgets($datafile_2));
    $time = intval(str_replace("\n", '', fgets($datafile_2)));
    $entry = floatval(str_replace("\n", '', fgets($datafile_2)));
    $stop = floatval(str_replace("\n", '', fgets($datafile_2)));
    $goal = floatval(str_replace("\n", '', fgets($datafile_2)));
    if($assetPair == 'XXBTZEUR' || $assetPair == 'XETHZEUR') {
        $goal = round($goal, 1, PHP_ROUND_HALF_DOWN);
    } else if($assetPair == 'XLTCZEUR') {
        $goal = round($goal, 2, PHP_ROUND_HALF_DOWN);
    } else if($assetPair == 'XXRPZEUR') {
        $goal = round($goal, 5, PHP_ROUND_HALF_DOWN);
    }
    $oneR = floatval(str_replace("\n", '', fgets($datafile_2)));
    //$txid = array();
    $sellVolume = 0;
    if(!$TEST_MODE) {
        //$txidstr = str_replace("\n", '', fgets($datafile_2));
        //$txid = explode(" ", $txidstr);
        $sellVolume = floatval(str_replace("\n", '', fgets($datafile_2)));
    }
    $analytics = str_replace("\n", '', fgets($datafile_2));
    fclose($datafile_2);
    $res = $kraken->QueryPublic('OHLC', array('pair' => $assetPair, 'interval' => 15));
    $res1 = $res['result'][$assetPair];
    $currBar = end($res1);
    $currTime = intval($currBar[0]);
    $currHigh = floatval($currBar[2]);
    $currClose = floatval($currBar[4]);
    $currR = ($currClose - $entry)/$oneR;
    print_r($assetPair);
    print_r("\n");
    print_r("Entry: ");
    print_r("\n");
    print_r($entry);
    print_r("\n");
    print_r("Stop: ");
    print_r("\n");
    print_r($stop);
    print_r("\n");
    print_r("Goal: ");
    print_r("\n");
    print_r($goal);
    print_r("\n");
    print_r("Current price: ");
    print_r("\n");
    print_r($currClose);
    print_r("\n");
    print_r("Current high: ");
    print_r("\n");
    print_r($currHigh);
    print_r("\n");
    print_r("One R: ");
    print_r("\n");
    print_r($oneR);
    print_r("\n");
    print_r("Current R: ");
    print_r("\n");
    print_r($currR);
    print_r("\n");
    if($currClose <= $stop && $currClose != 0.0) {
        $resultfile = fopen("log.txt", "a+");
        $resultR = ($currClose - $entry)/$oneR;
        $originalStop = $entry - $oneR;
        $formatted = sprintf("%s %s %g %g %g %g %g %s", $assetPair, $time, $entry, $originalStop, $goal, $resultR, $oneR, $analytics);
        fwrite($resultfile, $formatted);
        fwrite($resultfile, "\n");
        fclose($resultfile);
        $datafile_3 = fopen("data.txt", "w");
        fclose($datafile_3);
    } else if($currClose >= $goal) {
        $newGoal = $currHigh + $oneR;
        $datafile_3 = fopen("data.txt", "w");
        fwrite($datafile_3, $assetPair);
        fwrite($datafile_3, "\n");
        fwrite($datafile_3, $time);
        fwrite($datafile_3, "\n");
        fwrite($datafile_3, $entry);
        fwrite($datafile_3, "\n");
        fwrite($datafile_3, $goal);
        fwrite($datafile_3, "\n");
        fwrite($datafile_3, $newGoal);
        fwrite($datafile_3, "\n");
        fwrite($datafile_3, $oneR);
        fwrite($datafile_3, "\n");
        if(!$TEST_MODE) {
            fwrite($datafile_3, $sellVolume);
            fwrite($datafile_3, "\n");
        }
        fwrite($datafile_3, $analytics);
        fwrite($datafile_3, "\n");
        fclose($datafile_3);
        if(!$TEST_MODE) {
            $cancel = $kraken->QueryPrivate('CancelAll');
            if($cancel > 0) {
                $order = $kraken->QueryPrivate('AddOrder', array(
                    'pair' => $assetPair, 
                    'type' => 'sell', 
                    'ordertype' => 'stop-loss', 
                    'volume' => $sellVolume,
                    'price' => $goal
                ));
                $error = $order['error'];
                if(count($error) > 0) {
                    foreach($error as $err) {
                        $recordError = fopen("log.txt", "a+");
                        fwrite($recordError, $err);
                        fwrite($recordError, "\n");
                        fclose($recordError);
                        print_r($err);
                        print_r("\n");
                    }
                } else {
                    print_r($order['result']['descr']['order']);
                    print_r("\n");
                }
            }
        }
    }
}

function findLow($arr) {
    $lowest = $arr[0][3];
    foreach($arr as $bar) {
        $low = $bar[3];
        if($low < $lowest) {
            $lowest = $low;
        }
    }
    return $lowest;
}

function findHigh($arr) {
    $highest = $arr[0][3];
    foreach($arr as $bar) {
        $high = $bar[3];
        if($high > $highest) {
            $highest = $high;
        }
    }
    return $highest;
}

function countPivots($pivots, $stop, $distance) {
    $count = 0;
    foreach($pivots as $pivot) {
        $low = $pivot - $distance;
        $high = $pivot + $distance;
        if($stop <= $high && $stop >= $low) {
            $count += 1;
        }
    }
    return $count;
}

function balance() {
    global $kraken;
    $query = $kraken->QueryPrivate('Balance');
    print_r("Balance: \n");
    print_r($query);
    print_r("\n");
}

function openOrders() {
    global $kraken;
    $query = $kraken->QueryPrivate('OpenOrders', array('trades' => true));
    print_r("Open orders: \n");
    print_r($query);
    print_r("\n");
}

function tradeBalance() {
    global $kraken;
    $query = $kraken->QueryPrivate('TradeBalance');
    print_r("Trade balance: \n");
    print_r($query);
    print_r("\n");
}       

function entry($assetPair, $stop, $buyVolume) {
    global $kraken;
    $orders = $kraken->QueryPrivate('OpenOrders', array('trades' => true));
    $ordersArray = $orders['result']['open'];
    if(count($ordersArray) == 0) {
        $order = $kraken->QueryPrivate('AddOrder', array(
            'pair' => $assetPair, 
            'type' => 'buy', 
            'ordertype' => 'market', 
            'volume' => $buyVolume,
            'close[ordertype]' => 'stop-loss',
            'close[price]' => $stop
            ));
        $error = $order['error'];
        $output = "";
        if(count($error) > 0) {
            $output = "ERR " . $error[0];
        } else {
            $txid = $order['result']['txid'];
            $output = "OK " . $txid[0];
        }
        fwrite(STDOUT, json_encode($output));
    }
}

function raiseStop($assetPair, $goal, $sellVolume) {
    global $kraken;
    $cancel = $kraken->QueryPrivate('CancelAll');
    if($cancel > 0) {
        $order = $kraken->QueryPrivate('AddOrder', array(
            'pair' => $assetPair, 
            'type' => 'sell', 
            'ordertype' => 'stop-loss', 
            'volume' => $sellVolume,
            'price' => $goal
        ));
        $error = $order['error'];
        if(count($error) > 0) {
            $output = "ERR " . $error[0];
            fwrite(STDOUT, json_encode($output));
        } else {
            $txid = $order['result']['txid'];
            $output = "OK " . $txid[0];
            fwrite(STDOUT, json_encode($output));
        }
    }
}

function clear() {
    $datafile = fopen("data.txt", "w");
    fclose($datafile);
}

?>