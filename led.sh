#!/bin/bash

if [ $1 = "RED" ]
then
        curl  http://192.168.0.229:8080/CMD?LEDRED=ON
fi

if [ $1 = "GREEN" ]
then
        curl  http://192.168.0.229:8080/CMD?LEDGREEN=ON
fi

if [ $1 = "BLUE" ]
then
        curl  http://192.168.0.229:8080/CMD?LEDBLUE=ON
fi
