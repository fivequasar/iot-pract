# iot-pract (READ THE ENTIRE THING, before starting)

Each file represents an instance, do it by order:
1) mqtt_broker (authentication configured, TLS NOT configured):
   1) Contains bash steps to setup MQTT ONLY with authentication and logging enabled on the instance.
   
3) iot_sensor:
   1) Contains bash steps on configuring the instance
   2) Contains a 'aircon_light.py' python script to send data over to historianDB (make sure to read the code and understand)
       
4) historianDB:
   1) Contains bash steps on configuring the instance
   2) Contains a 'receiver.py' python script to receive data from iot_sensor (make sure to read the code and understand).
   3) Contains the database schema, initiate it on the web server
      
* While Creating all three instances, make sure that:
   1) OS: ubuntu, use the default AMI they provide.
   2) Instance Type: t2.micro
   3) Firewall (security groups): Enable: SSH, HTTP, HTTPS and MQTT (Port 1883) for all machines temporarily.
   * Note for the creation of security group please specify CUSTOM TCP and port 1883 FOR MQTT!
   * Also note that everytime you shutdown and startup an instance the public IP address WILL change, that means going to both python files ( 'aircon_light.py' and 'receiver.py' ) and change the IP addresses for the broker's ip.
   4) Use default VPC
   
* In your IFTT application, there should be two button widgets to control both the aircon and the lights, refer to 'aircon_light.py' to see the URL.
* Result: If all is working correctly, make sure that the aircon_light.py is running on the iot_sensor instance, run the mosquitto service with the default.conf running on the mqtt_broker instance and the receiver.py is running on the historian_db instance. Once all is running, click on your IFTT widget for either devices, and look at the receiver.py output on historian_db instance, it should show something like: 2023.04.11-15:59:12 aircon Off Temp=0


