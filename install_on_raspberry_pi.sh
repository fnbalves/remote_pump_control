#!/bin/bash

echo "INSTALLING DEPENDENCIES...."

cd control_server
chmod a+x scripts/*.sh

./scripts/install_dependencies.sh

python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser

cd ..

echo "CREATING STARTUP SERVICE...."

cp control_server/start_server.service start_server.service
cp control_server/systemd_command.sh systemd_command.sh
 
CURRENT_DIR=$(pwd)
COMMAND="s+service_path+${CURRENT_DIR}+g"
sed -i $COMMAND start_server.service
sed -i $COMMAND systemd_command.sh

chmod a+x systemd_command.sh

sudo cp start_server.service /etc/systemd/system
sudo systemctl enable start_server.service

echo "DONE"

