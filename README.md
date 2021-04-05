# DiscoballTime
Use Alexa to trigger a discoball to drop from a trapdoor in the ceiling, using motors and other home automation tools to open &amp; close trapdoors, lower &amp; raise the discoball, turn on &amp; off the discoball rotation and ambiance lights.


Hello world!



### Setup

ssh-keygen -t rsa -b 2048 
    follow the prompts there to save the keys
ssh-copy-id pi@192.168.0.43
    copy it to the target.  Now password not needed

now run `bash sync_rpi.sh 192.168.0.43` to sync the DiscoballTime dir between systems
(Drawback - doesn't delete files, just create/updates files.  So occassional delete on pi system necessary)

AWS IOT docu - https://aws.github.io/aws-iot-device-sdk-python-v2/ 

##### Hardware setup

Follow instructions: https://docs.aws.amazon.com/iot/latest/developerguide/connecting-to-existing-device.html
basically downloading .pem files to pi

on AWS IoT - Create a policy with create/connect/sub/pub rights 
create a thing (download .pem) and attach policy to the corresponding certificate 
drops certs in it's own dir

Now the thing can securely communicate with aws iot core

#### In order to autorun the script at start:
https://www.raspberrypi.org/documentation/linux/usage/systemd.md

``` sudo systemctl stop discoball.service```
sudo cp /home/pi/DiscoballTime/discoball.service /etc/systemd/system/discoball.service

alias discoSync="sudo cp /home/pi/DiscoballTime/discoball.service /etc/systemd/system/discoball.service && sleep 1 && sudo systemctl daemon-reload"
alias discoStatus="sudo systemctl status discoball.service"
alias discoStart="sudo systemctl start discoball.service"
alias discoStop="sudo systemctl stop discoball.service"
alias discoReset="echo 'syncing service...' && discoSync && echo 'stopping...' && discoStop && sleep 2 && echo 'starting...' && discoStart && sleep 3 && discoStatus"

these are nice helper functions saved to: nano ~/.bash_aliases




## The Story 

Discoball bought 
Raspberry pi chosen 
Motor selection difficult (Fred can fill in more here) 
    * Stepper motors chosen for their precision
    * Motor power driver, be able to move sufficient weight 
Motor can hold weight if left 'on', but without leaving the magnet spinning it cannot hold more than a few pounds of pressure
    * Debated  adding another motor to act as a clamp, or another electric system which would engage a ratchet which would leverage a mechanical system to hold the weight up, or a complex mechanical system so that only one motor does the door/discoball and the 2nd motor could act as a clamp
    * Ended up adding a counter balance component to the discoball so that the effective torque on the motor is 0



#### final setup Notes 

Quite a bit of work to integrate into controlling the tp-link kasa smart plug 