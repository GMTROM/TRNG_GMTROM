in this folder you can find all needed files to run the REST Interface and all code that runs on the Raspberry Pi 


Installing Nginx Server:
sudo apt install nginx

Setting up Flask or REST API Framework:
pip install flask

Creating SSL Certificates:
1. Open the terminal on your Raspberry Pi.
2. Execute the following command to generate a new SSL certificate and its corresponding private key:
openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout server.key -out server.crt

3. This command generates a self-signed certificate (server.crt) and the private key (server.key). You will be prompted to enter some information such as country, location, organization, etc. You can fill in the information as needed.
4. After generating the certificate and key, you should copy the respective files to your Nginx server. A common method is to copy them to the directory /etc/nginx/ssl using the following command:
sudo cp server.crt server.key /etc/nginx/ssl/

5. Editing Default Page Redirect (/etc/nginx/sites-available/default):
sudo nano /etc/nginx/sites-available/default

6. Locate the server block to which your REST service belongs, and add the following lines to configure the SSL certificate and key:
server {
	listen 443 ssl;
        server_name 172.16.78.57;

	ssl_certificate /etc/nginx/ssl/cert-gmtrom.pem;
	ssl_certificate_key /etc/nginx/ssl/cert-gmtrom-key.pem;

	root /var/www/html;
	index index.html;

	location /trng {
		proxy_pass https://172.16.78.57:5000;  
		proxy_set_header Host $host;
		proxy_set_header X-Real-IP $remote_addr;
	}  
}

Make sure to provide the correct file paths if you copied them to a different location.

7. Save the changes and close the text editor.
8. Verify the Nginx configuration for errors:
sudo nginx -t
If no errors are reported, proceed to the next step. Otherwise, review the configuration for possible errors.

9. Restart the Nginx server to apply the changes:
sudo service nginx restart

Configuring Static IP:
Setting up a static IP address on a Raspberry Pi depends on your operating system. Here are the steps for the two most common operating systems:

For Raspbian/Raspberry Pi OS:
- Open the terminal application on your Raspberry Pi.
- Edit the DHCP client configuration file using the command:
sudo nano /etc/dhcpcd.conf

- Look for the section starting with "# Example static IP configuration."
- Uncomment the lines below it starting with "interface" and "static ip_address" by removing the '#'.
- Adjust the values for "interface" (e.g., eth0 or wlan0), "static ip_address" (e.g., 192.168.1.10/24), "static routers" (gateway IP address), and "static domain_name_servers" (DNS server IP address) according to your network configuration.
- Save the file (Ctrl + O) and exit the editor (Ctrl + X).
- Restart your Raspberry Pi for the changes to take effect.


Optional:
Setting up a virtual environment for Flask server:
python3 -m venv venv
source venv/bin/activate

Checking if port 443 is open (using Telnet):
sudo apt-get install telnet



Setting up uWSGI server:
sudo apt-get install uwsgi

First change the Location mentionend above with this: (in /etc/nginx/sites-available/default)
location /trng {
		include uwsgi_params;
		uwsgi_pass 127.0.0.1:5000;  # Weiterleitung an uWSGI
	}
Then u need to use the uwsgi.ini and uwsgi.service File provided in the UWSGI folder.
In our testing the uWSGI Server with 1 Worker (because I2C cant handle multithreading) is slower than the Flask Development Server.
Because our Application is not used in a Production Environment we kept the Flask Development Server for Performance.
