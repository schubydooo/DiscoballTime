echo "Syncronizing DiscoballTime dir from this computer to the Pi..."

rsync -avz -e ssh ~/Documents/GitHub/DiscoballTime/ pi@$1:DiscoballTime/ 
