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