In this folder you can find all needed files to configure the Raspberry Pi 3 

A Zip-File with an OS and all necessary configurations can be found here: https://drive.google.com/file/d/1j7z5_xab89vaT2T0lru3GgnLtOAT9Vaj/view?usp=sharing
If you use this file no additional changes need to be done on the Raspberry Pi.


Alternativly you can configure your own OS by following the steps below:

To ensure that the Nginx server and Flask application start automatically when the Raspberry Pi boots up, you can configure a systemd service.

Here are the steps to achieve this:

1. Create a service configuration file for the Nginx server. Create a file named `nginx.service` in the directory `/etc/systemd/system/` (e.g., `/etc/systemd/system/nginx.service`), and insert the following content:

[Unit]
Description=Nginx HTTP server
After=network.target

[Service]
ExecStart=/usr/sbin/nginx -g "daemon off;"
ExecReload=/usr/sbin/nginx -s reload
ExecStop=/usr/sbin/nginx -s stop
Restart=on-failure
KillMode=process
PrivateTmp=true

[Install]
WantedBy=multi-user.target

2. Create a service configuration file for the Flask application. Create a file named `flaskapp.service` in the directory `/etc/systemd/system/` (e.g., `/etc/systemd/system/flaskapp.service`), and insert the following content:

[Unit]
Description=Flask Application
After=network.target

[Service]
WorkingDirectory=/path/to/flask-project
ExecStart=/path/to/venv/bin/python /path/to/flask-project/app.py
Restart=on-failure
User=username
Group=usergroup

[Install]
WantedBy=multi-user.target

Make sure to adjust the paths according to your actual configuration. Also, note that you need to provide the path to the virtual environment (`/path/to/venv/bin/python`) and the path to the main file of the Flask application (`/path/to/flask-project/app.py`). Additionally, replace "username" and "usergroup" with the name of the user and group under which the Flask application should run.

3. Update the systemd service configuration. Execute the following commands to update the systemd service configurations and enable the services:

sudo systemctl daemon-reload
sudo systemctl enable nginx
sudo systemctl enable flaskapp

4. Start the services. Start the Nginx and Flask app services using the following commands:

sudo systemctl start nginx
sudo systemctl start flaskapp

This will automatically start the Nginx server and Flask application when the Raspberry Pi boots up. You can check the status of the services to ensure they started properly by executing the commands `sudo systemctl status nginx` and `sudo systemctl status flask-app`.

Please note that the exact steps may vary depending on your specific configuration and the Raspberry Pi's operating system. The above steps assume a Linux-based operating system. Make sure to make the necessary adjustments according to your environment.
