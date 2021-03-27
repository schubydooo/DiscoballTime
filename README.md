# DiscoballTime
Use Alexa to trigger a discoball to drop from a trapdoor in the ceiling, using motors and other home automation tools to open &amp; close trapdoors, lower &amp; raise the discoball, turn on &amp; off the discoball rotation and ambiance lights.


Hello world!



### Setup

ssh-keygen -t rsa -b 2048 
    follow the prompts there to save the keys
ssh-copy-id pi@192.168.0.43
    copy it to the target.  Now password not needed

now run `bash sync_rpi.sh 192.168.0.43` to sync the DiscoballTime dir between systems
