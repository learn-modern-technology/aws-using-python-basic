#!/bin/bash 
APP_NAME=LiftShift-Application
sudo apt update -y && sudo apt -y install python3-pip zip
cd /opt
sudo wget https://d6opu47qoi4ee.cloudfront.net/loadbalancer/simuapp-v1.zip
sudo unzip simuapp-v1.zip
sudo rm -f simuapp-v1.zip
sudo sed -i "s=MOD_APPLICATION_NAME=$APP_NAME=g" templates/index.html
sudo pip3 install -r requirements.txt
sudo nohup python3 simu_app.py >> application.log 2>&1 &