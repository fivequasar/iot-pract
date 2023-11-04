#!/usr/bin/python3

import dweepy
import time
import os


link_air = "4640D_air_con_sensor"; # ensure that when you use IFTT, https://dweet.io/dweet/for/4640D_air_con_sensor?status=onoff is the url for your web hook application

link_light = "4640D_light_sensor"; # ensure that when you use IFTT, https://dweet.io/dweet/for/4640D_light_sensor?status=onoff is the url for your web hook application

host = "54.169.180.83"; # broker's ip

mqtt_username = "4640D_user"; # mqtt user that was created on mqtt_server.

mqtt_password = "4640D_password"; # mqtt password that was created on mqtt_server.


query_air_state = input("Air con on or off? ");

query_air_read = input("Reading? ");

query_air_state_low_cap = query_air_state.lower();

query_air_read_num_to_string = str(query_air_read);



query_light_state = input("Light on or off? ");

query_light_bright = input("Brightness? ");

query_light_state_low_cap = query_light_state.lower();

query_light_bright_num_to_string = str(query_light_bright);



if query_air_state_low_cap == "on":
        
        print("Air-conditioner is on!");
        result = dweepy.dweet_for(link_air, {'status': 'on', 'temp': query_air_read_num_to_string});
        currentAirTimeStamp = result['created'];
        
elif query_air_state_low_cap == "off":
        
        print("Air-conditioner is off!");
        result = dweepy.dweet_for(link_air, {'status': 'off', 'temp': '0'});
        currentAirTimeStamp = result['created'];
        
else:
    
        print("Program Terminated");
        


if query_light_state_low_cap == "on":
    
        print("Light is on!");
        result = dweepy.dweet_for(link_light, {'status': 'on', 'brightness': query_light_bright_num_to_string});
        currentLightTimeStamp = result['created'];

elif query_light_state_low_cap == "off":
    
        print("Light is off!");
        result = dweepy.dweet_for(link_light, {'status': 'off', 'brightness': '0'});
        currentLightTimeStamp = result['created'];
    
else:
    
        print("Program Terminated");
        

while True:
    
    latestDweetAir = dweepy.get_latest_dweet_for(link_air);
    latestDweetLight = dweepy.get_latest_dweet_for(link_light);
    
    latestDweetTimeStampAir = latestDweetAir[0]['created'];
    latestDweetTimeStampLight = latestDweetLight[0]['created'];
    
    if latestDweetTimeStampAir != currentAirTimeStamp: 
        
        currentAirTimeStamp = latestDweetTimeStampAir
        
        if query_air_state == "off": 
            #print("Received new dweet on", latestDweetAir[0]['created']);
            print("Air-conditioner is on!");
            print("Brightness is at " + query_air_read_num_to_string);
            os.system("mosquitto_pub -d -h " + host + " -u " + mqtt_username + " -P " + mqtt_password + " -t brokerchannel -m '" + latestDweetTimeStampAir + "_aircon_on" + query_air_read_num_to_string + "';");
            query_air_state = "on"

        
        elif query_air_state == "on":
            #print("Received new dweet on", latestDweetAir[0]['created']);
            print("Air-conditioner is off!");
            os.system("mosquitto_pub -d -h " + host + " -u " + mqtt_username + " -P " + mqtt_password + " -t brokerchannel -m '" + latestDweetTimeStampAir + "_aircon_of0';");
            query_air_state = "off"
            
    time.sleep(1) 
    
    if latestDweetTimeStampLight != currentLightTimeStamp: 
        
        currentLightTimeStamp = latestDweetTimeStampLight
        
        if query_light_state == "off": 
            #print("Received new dweet on", latestDweetLight[0]['created']);
            print("Light is on!");
            print("Brightness is at " + query_light_bright_num_to_string);
            os.system("mosquitto_pub -d -h " + host + " -u " + mqtt_username + " -P " + mqtt_password + " -t brokerchannel -m '" + latestDweetTimeStampLight + "_lights_on" + query_light_bright_num_to_string +"';");
            query_light_state = "on"
            

        
        elif query_light_state == "on":
            #print("Received new dweet on", latestDweetLight[0]['created']);
            print("Light is off!");
            os.system("mosquitto_pub -d -h " + host + " -u " + mqtt_username + " -P " + mqtt_password + " -t brokerchannel -m '" + latestDweetTimeStampLight + "_lights_of0';");
            query_light_state = "off"
            
        
    time.sleep(1)