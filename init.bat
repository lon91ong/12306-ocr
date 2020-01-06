cd %~dp0
wsl sudo chmod 777 start.sh
wsl sudo apt-get install libsm6
wsl sudo pip install -r ./requirements.txt