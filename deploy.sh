REPOSITORY=/home/ubuntu/HibiscusSyriacusExplorer
cd $REPOSITORY

APP_NAME=action_codedeploy

CURRENT_PID=$(pgrep -f $APP_NAME)

if [ -z "$CURRENT_PID" ]
then
  echo "> 종료할것 없음."
else
  echo "> kill -9 $CURRENT_PID"
  kill -15 "$CURRENT_PID"
  sleep 5
fi

# pipenv install 을 위해 가상 메모리 1G 할당
sudo fallocate -l 1G /swapfile
sudo chmod 600 /swapfile
sudo mkswap  /swapfile
sudo swapon /swapfile
sudo swapon  --show
sudo free -h

# start server with pipenv
sudo apt update -y
sudo apt install python3-pip -y
sudo apt install pipenv -y
pipenv --python 3.10
pipenv sync
pipenv run nohup uvicorn src.app:app --port 8000 --host 0.0.0.0 --reload > uvicorn.log 2>&1 &

exit 0