rm alexa-deployment.zip
cd alexa-skill/
zip -X -r ../alexa-deployment.zip *
cd ..
clear
echo "------------alexa-deployment.zip package created---------------"

aws lambda update-function-code --function-name DiscoballTime --zip-file fileb://alexa-deployment.zip

