#!/bin/bash
sudo pip3 install virtualenv
cd /home/ec2-user/app
virtualenv venv
source venv/bin/activate
sudo pip3 install -r requirements.txt