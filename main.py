import sys
from Adafruit_IO import MQTTClient                                                                                                                                                                       
import time
import json
from fsm import *
                                                                                                                                                       
                                                                                                                                                       
# Update the Adafruit IO configurations-
                                                                                                                                                     
AIO_FEED_IDs = ["nutnhan1","nutnhan2","nutnhan3"]
AIO_USERNAME = "HThuanN"
AIO_KEY = "aio_qztQ70a8LX30imG1i0gzwbeDeeu9"

# Define the file path for the scheduler data-

SCHEDULER_FILE_PATH = 'schedulers.txt'
                                                                                                                                                       
                                                                                                                                                       
def load_schedules_from_file(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return [

        irrigation_schedule(**data['sched1']),
        irrigation_schedule(**data['sched2']), 
        irrigation_schedule(**data['sched3']) 
                                                                                          
    ] 
                                                                                                                                                       
                                                                                                                                                       
# Load schedules from the file at the start                                                                                                                         
schedules = load_schedules_from_file(SCHEDULER_FILE_PATH)
def connected(client):
    print("Ket noi thanh cong ...")  
    for topic in AIO_FEED_IDs: 
        client.subscribe(topic) 
                                                                                                                
def subscribe(client, userdata, mid, granted_qos): 
    print("Subscribe thanh cong ...") 
                                                                                                                                                       
def disconnected(client):    
    print("Ngat ket noi ...")  
    sys.exit(1) 
                                                                                                                                                       
                                                                                                                                                       
def message(client, feed_id, payload):                                                                                                       
    print("\nNhan du lieu: " + payload + " feed id: " + feed_id) 

    global schedules    
    if feed_id == "nutnhan1" and payload == '0': 
        schedules[0].isActive = False  
        schedules[0].print_data()
    elif feed_id == "nutnhan1" and payload == '1': 
        schedules[0].isActive = True 
        schedules[0].print_data() 
    if feed_id == "nutnhan2" and payload == "0":                                                                                             
        schedules[1].isActive = False  
        schedules[1].print_data()  
    elif feed_id == "nutnhan2" and payload == "1":                                                                                                 
        schedules[1].isActive = True  
        schedules[1].print_data()  
    if feed_id == "nutnhan3" and payload == "0":  
        schedules[2].isActive = False                                                                                                      
        schedules[2].print_data()                                                                                                     
    elif feed_id == "nutnhan3" and payload == "1":
        schedules[2].isActive = True   
        schedules[2].print_data()   
                                                                                                                                                       
client = MQTTClient(AIO_USERNAME, AIO_KEY)
client.on_connect = connected  
client.on_disconnect = disconnected 
client.on_message = message  
client.on_subscribe = subscribe
client.connect()  
client.loop_background()    

while True:
    fsm(schedules, client)
    time.sleep(1)  