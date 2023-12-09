#!/usr/bin/python3

import paho.mqtt.client as mqtt

import mysql.connector;
import os
from flask import Flask, request, redirect
import ssl
dna = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
dna.load_cert_chain('cert.pem', 'key.pem')

#from dotenv import load_dotenv
#load_dotenv()  # take environment variables from .env.

#aws_host = os.getenv('host')
#aws_user = os.getenv('user')
#aws_pass = os.getenv('password')

mydb = mysql.connector.connect(
    host="iot-project-db.cghvznng7oe0.us-east-1.rds.amazonaws.com", #RDS's DNS address
    user="admin",
    password="iot-project-password"
)


#flask app
app = Flask(__name__)

#mqtt sub to mqtt server
def on_connect(client, userdata, flags, rc):   
    client.subscribe("brokerchannel")
    

def on_message(client, userdata, msg):
    message = msg.payload.decode("utf-8")
    
    reading = message[34:]
    
    original_date = message [0:10]
    
    original_time = message [11:19]
    
    name = message[25:31]
    
    state = message[32:34]

    month_date = original_date[8:10]
    
    day_date = original_date[5:7]
    
    year_date = original_date[0:4]
    
    modified_date = year_date + "." + month_date + "." + day_date
    
    modified_timestamp = modified_date + "-" + original_time
    
    
    if state == "on":
        
        state = "On"
        
    elif state == "of":
        
        state = "Off"
        
        
    if name == "aircon":
        
       mycursor = mydb.cursor()
       reading = "Temp=" + message[34:]
       sql_update = "UPDATE historianDB.iot_devices SET status = %s, reading = %s, time_stamp = %s WHERE no = %s"
       val = (state, reading, modified_timestamp, 1)
       mycursor.execute(sql_update, val)
       mydb.commit()
        
    elif name == "lights":
        
       mycursor = mydb.cursor()
       reading = "Brightness=" + message[34:]
       sql_update = "UPDATE historianDB.iot_devices SET status = %s, reading = %s, time_stamp = %s WHERE no = %s"
       val = (state, reading, modified_timestamp, 2)
       mycursor.execute(sql_update, val)
       mydb.commit()

        
    print(modified_timestamp + " " + name + " " + state + " " + reading)



#flask route
@app.route("/")
def default():
    try:
        cursor = mydb.cursor()
        query = ("""SELECT * FROM historianDB.iot_devices """)
        cursor.execute(query)
        comments = cursor.fetchall()
        #mydb.close()
        completeTable="<tr>"
        completeTable += "<td> No. </td>"
        completeTable += "<td> Time Stamp</td>"
        completeTable += "<td> Device</td>"
        completeTable += "<td> Status </td>"
        completeTable += "<td> Reading </td>"
        completeTable+="</tr>"
        for c in comments:
            completeTable+="<tr>"
            completeTable += "<td>" + str(c[0]) + "</td>"
            completeTable += "<td>" + str(c[1]) + "</td>"
            completeTable += "<td>" + str(c[2]) + "</td>"
            completeTable += "<td>" + str(c[3]) + "</td>"
            completeTable += "<td>" + str(c[4]) + "</td>"
            completeTable+="</tr>"
        return """
        <html>
        <body>
            <p>Sensors data</p>
            <table border=\"1\">
            %s
            </table>
        </body>
        </html>
        """ %(completeTable)
    except:
        return redirect("https://http.cat/404")

    
#flask serve
if __name__ == "__main__":
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.username_pw_set("4640D_user", "4640D_password") # mqtt user and password that was created on mqtt_server.
    client.connect("44.221.118.197", 1883); # broker's IP address.
    client.loop_start()
    #serve(app,host="0.0.0.0",port=443)
    #app.run(ssl_context=("cert.pem", "key.pem"))
    app.run(host='0.0.0.0',port=443,debug=False,ssl_context=dna)
