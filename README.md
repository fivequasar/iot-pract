# iot-pract
* READ THE ENTIRE THING *
Each file represents an instance, do it by order:
1) mqtt_broker (authentication configured, TLS NOT configured):
   1) Contains bash steps to setup MQTT ONLY with authentication and loggin enabled.
   
3) iot_sensor:
   1) Contains bash steps on configuring the instance
   2) Contains a 'aircon_light.py' python script to send data over to historianDB (make sure to read the code and understand)
       
4) historianDB:
   1) Contains the database schema, initiate it on the web server
   2) Contains a 'receiver.py' python script to receive data from iot_sensor (make sure to read the code and understand).
 
      
* Also note that everytime you shutdown and startup an instance the public IP address WILL change, that means going to both python files ( 'aircon_light.py' and 'receiver.py' ) and change the IP addresses for the broker's ip.
* In your IFTT application, there should be two button widgets to control both the aircon and the lights, refer to 'aircon_light.py' to see the URL.
* IMPORTANT, ALL INSTANCE ARE RUNNING UBUNTU, DO NOT USE AMAZON LINUX 2
