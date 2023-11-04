#!/usr/bin/python3

import paho.mqtt.client as mqtt

# PLEASE REFER TO LINE 81 and 82 *IMPORTANT*
# currently the sql connectors are all commented out, this is for convenience sake when you are doing the mysql, i assure you that it works if the request is sent from the iot_sensor, it will 
# change the data if the given schema is used. 

# import mysql.connector;

# mydb = mysql.connector.connect(
 # host="localhost", #RDS's DNS address
 # user="admin",
 # password="password"
# )

def on_connect(client, userdata, flags, rc):
    
    client.subscribe("brokerchannel");
    

def on_message(client, userdata, msg):
    
    message = msg.payload.decode("utf-8");
    
    reading = message[34:];
    
    original_date = message [0:10];
    
    original_time = message [11:19]
    
    name = message[25:31];
    
    state = message[32:34];
    
    month_date = original_date[8:10];
    
    day_date = original_date[5:7];
    
    year_date = original_date[0:4];
    
    modified_date = year_date + "." + month_date + "." + day_date
    
    modified_timestamp = modified_date + "-" + original_time
    
    
    if state == "on":
        
        state = "On";
        
    elif state == "of":
        
        state = "Off";
        
        
    if name == "aircon":
        
       # mycursor = mydb.cursor();
       reading = "Temp=" + message[34:];
       # sql_update = "UPDATE historianDB.iot_devices SET status = %s, reading = %s, time_stamp = %s WHERE no = %s"
       # val = (state, reading, modified_timestamp, 1);
       # mycursor.execute(sql_update, val);
       # mydb.commit();
        
    elif name == "lights":
        
       # mycursor = mydb.cursor();
       reading = "Brightness=" + message[34:];
       # sql_update = "UPDATE historianDB.iot_devices SET status = %s, reading = %s, time_stamp = %s WHERE no = %s"
       # val = (state, reading, modified_timestamp, 2);
       # mycursor.execute(sql_update, val);
       # mydb.commit();

        
    print(modified_timestamp + " " + name + " " + state + " " + reading);

    
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.username_pw_set("4640D_user", "4640D_password") # mqtt user and password that was created on mqtt_server.
client.connect("54.169.180.83", 1883); # broker's IP address.

client.loop_forever();

