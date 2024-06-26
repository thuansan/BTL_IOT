from datetime import datetime, timedelta
from rs485 import *
import json
                                                                                                                                        
                                                                                                                                                       
class irrigation_schedule:

    def __init__(self, cycle, flow1, flow2, flow3, isActive, schedulerName, startTime, stopTime):                                                                                                                                          
        self.cycle = cycle
        self.flow1 = flow1
        self.flow2 = flow2
        self.flow3 = flow3
        self.isActive = isActive
        self.schedulerName = schedulerName
        self.startTime = startTime
        self.stopTime = stopTime
                                                                                                                                                       
    def print_data(self):

        print("Cycle:", self.cycle)
        print("Flow 1:", self.flow1)
        print("Flow 2:", self.flow2)
        print("Flow 3:", self.flow3)
        print("Is Active:", self.isActive)
        print("Scheduler Name:", self.schedulerName)
        print("Start Time:", self.startTime)
        print("Stop Time:", self.stopTime)

def load_schedules_from_file(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)

    return [
        irrigation_schedule(**data['sched1']),
        irrigation_schedule(**data['sched2']),
        irrigation_schedule(**data['sched3'])
    ]

                                                                                                                                                       
schedules = load_schedules_from_file('schedulers.txt')
# Print the details of each schedule to verify-
                                                                                                                                                       
for schedule in schedules:
    schedule.print_data()
                                                                                                                                                       
IDLE = 0
MIXER1 = 1
MIXER2 = 2
MIXER3 = 3
PUMP_IN = 4
SELECTOR = 5
PUMP_OUT = 6
NEXT_CYCLE = 7
END = 8
                                                                                                                                                       
timeProcess = 0
sched_id = 0
state = IDLE
cycle = 0
timer_count = 0
last_serial_read_time = datetime.now()
serial_read_interval = timedelta(seconds=10)
started = False
area_selected = -1
wait = 1
                                                                                                                                                       
def area_selector(area):
                                                                                                                                                       
    if area == 0:                                                                                                                                                                                                                                                                               
        setDeviceON(4)
        setDeviceOFF(5)
        setDeviceOFF(6)
                                                                                                                                                       
    elif area == 1:
        setDeviceOFF(4)
        setDeviceON(5)
        setDeviceOFF(6)
                                                                                                                                                       
    elif area == 2:
        setDeviceOFF(4)
        setDeviceOFF(5)
        setDeviceON(6)
                                                                                                                                                                
def publish_stage(client, id, cycle, state):
    message = f"{id},{cycle},{state}"
    client.publish("stage", message)

def fsm(schedules, client):
    global state, cycle, timer_count, sched_id, started, area_selected, wait, last_serial_read_time
    current_time = datetime.now()

    # Read serial data every 10 

    if current_time - last_serial_read_time >= serial_read_interval:
        readSerial(client)
        last_serial_read_time = current_time

    if not schedules[sched_id].isActive:
        print(f"Schedule {sched_id} is not active")
        sched_id = (sched_id + 1) % 3
        state = IDLE
        wait = 1

    current_time_str = (current_time + timedelta(hours=6)).strftime("%H:%M")
    if started and schedules[sched_id].stopTime == current_time_str:
        sched_id = (sched_id + 1) % 3
        started = False
        state = IDLE
        wait = 1

    if state == IDLE:
            print("IDLE")
            print("Waiting for next schedule\n")
            wait = 0

    if schedules[sched_id].startTime == current_time_str:
            wait = 1
            print(f"Schedule {sched_id} is active now\n")
            started = True
            state = MIXER1
            timer_count = schedules[sched_id].flow1
            print(f"CYCLE: {cycle}")
            print("MIXER1")
            setDeviceON(1)
            publish_stage(client, sched_id, cycle, state)
            print(f"TimeProcess: {timer_count}")

    elif state == MIXER1:

        if timer_count <= 0:
            setDeviceOFF(1)
            print("MIXER2")
            state = MIXER2
            timer_count = schedules[sched_id].flow2
            setDeviceON(2)
            publish_stage(client, sched_id, cycle, state)
        print(f"TimeProcess: {timer_count}")

    elif state == MIXER2:

        if timer_count <= 0:
            setDeviceOFF(2)
            print("MIXER3")
            state = MIXER3
            timer_count = schedules[sched_id].flow3
            setDeviceON(3)
            publish_stage(client, sched_id, cycle, state)
        print(f"TimeProcess: {timer_count}")

    elif state == MIXER3:
        if timer_count <= 0:
            setDeviceOFF(3)
            print("PUMP_IN")
            state = PUMP_IN
            timer_count = 5
            setDeviceON(7)
            publish_stage(client, sched_id, cycle, state)
        print(f"TimeProcess: {timer_count}")
                                                                                                                                                       
    elif state == PUMP_IN:

        if timer_count <= 0:
            setDeviceOFF(7)
            print("SELECTOR")
            state = SELECTOR
            if area_selected == -1:
                area_selected = cycle % 3
            print(f"Area selected: {area_selected}")
            timer_count = 2
            publish_stage(client, sched_id, cycle, state)
        print(f"TimeProcess: {timer_count}")
                                                                                                                                                       
    elif state == SELECTOR:
                                                                                                                                                       
        if timer_count <= 0:
            print("PUMP_OUT")
            state = PUMP_OUT
            timer_count = 5
            setDeviceON(8)
            publish_stage(client, sched_id, cycle, state)
        print(f"TimeProcess: {timer_count}")
                                                                                                                                                       
    elif state == PUMP_OUT:

        if timer_count <= 0:
            setDeviceOFF(8)
            print("NEXT_CYCLE")
            state = NEXT_CYCLE
            publish_stage(client, sched_id, cycle, state)
        print(f"TimeProcess: {timer_count}")
                                                                                                                                                                                                                                                                                             
    elif state == NEXT_CYCLE:
        cycle += 1
        if cycle < schedules[sched_id].cycle:
            state = MIXER1
            timer_count = schedules[sched_id].flow1
            print(f"CYCLE: {cycle}")
            print("MIXER1")
            setDeviceON(1)
            publish_stage(client, sched_id, cycle, state)
            print(f"TimeProcess: {timer_count}")
                                                                                                                                                       
        else:                                                                                                                                                                                                                                                                                    
            print("END SCHEDULE")
            area_selected = -1
            started = False
            sched_id = (sched_id + 1) % 3
            state = IDLE
            cycle = 0
            if sched_id == 0:
                print("END")

    timer_count -= 1