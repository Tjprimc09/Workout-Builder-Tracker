import csv
import os
import datetime

'''
I am building this application because I want to create and track my own athletic training program. 
This is an exercise in OOP design and implementation, using domains I am familiar with.

A training program consists of a training schedule (or multiple schedules over time), 
a training schedule has certain training protocols (like full body strength, full body HIIT, etc) scheduled on certain days,
protocols have different phases/blocks (like warmup, main block, cool down), 
phases have specific exercises, 
exercises are tracked in sets (meaning exercises own sets), which contain performance data. 
'''


# I'll start with a training program class that can hold multiple training schedules. This is the highest level object in the hierarchy.
class trainingProgram():
    def __init__(self, name = "Unnamed Training Program"):
        self.name = name
        self.schedules = []

    def add_schedule(self, newSchedule):
        self.schedules.append(newSchedule)

    def remove_schedule(self, remove):
        self.schedules.pop(remove)

    def clear_schedules(self):
        self.schedules.clear()

    def __str__(self):
        text = f"Training Program: {self.name}\n\nTraining Schedules:\n\n"
        for i, schedule in enumerate(self.schedules, start = 1):
            line = f"Schedule {i}: {schedule.name}"#\n\n{schedule}\n\n"
            text += line

        return text



'''
Next in the hierarchy is the training schedule class.
A training schedule class consists of a start date, a split (list of protocol objects), number of cycles to repeat the split, and training days of the week. 
A training schedule object should be able to map the split to the training days over the specified number of cycles, 
skipping rest days if the training day falls on a rest day, and filling in rest days if a training day falls on a non-training day.
'''
class trainingSchedule():
    def __init__(self, name = "Unnamed Schedule", startDate = None, split = None, cycles = None, trainingDays = None):
        self.name = name
        self.startDate = datetime.date.today() if startDate is None else startDate
        self.endDate = None
        self.split = ["Full body posture correction", "Full body mobility", "Rest", "Full body HIIT", "Functional core", "Rest", "Full body strength", "Full body flexibility", "Rest"] if split is None else split #default to beginner-facing full body athletic training split
        self.cycles = 12 if cycles is None else cycles
        self.trainingDays = ["Monday", "Tuesday", "Friday", "Saturday"] if trainingDays is None else trainingDays #using my own training schedule as default
        self.schedule = {}

        self.map_split_to_trainingDays() #automatically map the split to the training days upon initialization
    
    def update_start(self, newStart):
        self.startDate = newStart
        self.schedule.clear() #reset the schedule
        self.map_split_to_trainingDays() #remap the split to the training days from the new start date

    def insert_split(self, newSplit, index):
        self.split.insert(index, newSplit)
        self.schedule.clear()
        self.map_split_to_trainingDays()

    def remove_split(self, remove):
        self.split.pop(remove)
        self.schedule.clear()
        self.map_split_to_trainingDays()

    def clear_split(self):
        self.split.clear()
        self.schedule.clear()
        self.map_split_to_trainingDays()

    def update_trainingDays(self, days):
        self.trainingDays = days
        self.schedule.clear()
        self.map_split_to_trainingDays()

    def map_split_to_trainingDays(self):
        date = self.startDate #for output tracing, assume startDate is Thursday, 1/1/2026. Also assume default attributes for cycles, split, and M,T,F,S for trainingDays
        weekdayMap = {
            "Monday": 0,
            "Tuesday": 1,
            "Wednesday": 2,
            "Thursday": 3,
            "Friday": 4,
            "Saturday": 5,
            "Sunday": 6
            }
        
        trainingDays = [weekdayMap[day] for day in self.trainingDays]

        for i in range(self.cycles): #for each defined cycle (default to 12 cycles)
            
            for protocol in self.split: #loop through each protocol in the split
                
                if protocol.lower() == 'rest': #if the protocol is rest...
                    
                    if date.weekday() in trainingDays: #check if the current date is a scheduled training day
                        #if it is, skip to the next protocol without adding the rest protocol, because we prefer to train if the day allows it
                        #print("Scheduled a training protocol to comply with your training days setting, skipping rest protocol")
                        continue

                    else: #if it's not a training day, we can add the rest day
                        #print("Adding rest protocol")
                        self.schedule[date] = protocol
                        date += datetime.timedelta(days=1) #iterate to the next day after scheduling a rest day
                        continue #and move to the next protocol
                else: #if it's not a rest protocol...
                    while date.weekday() not in trainingDays: #check if the current day is a scheduled training day 
                        #print("Scheduling rest protocol to fill non-training day")
                        self.schedule[date] = "Rest" #if it's not a scheduled training day, then the protocol for that day is rest
                        date += datetime.timedelta(days=1) #then iterate until we find a training day
                    #print("Scheduling training protocol")
                    self.schedule[date] = protocol #once we find a training day, we can schedule the protocol
                    date += datetime.timedelta(days=1) #move to the next day after scheduling a training protocol
                    continue #move to the next protocol
        self.endDate = date - datetime.timedelta(days=1) #the end date is the last scheduled date, which is one day before the current date after exiting the loop
    
    def __str__(self):
        text = f"Start date: {self.startDate}\n\nWeekly training days: {', '.join(self.trainingDays)}\n\n{self.cycles} cycle training schedule:\n\n"
        for k,v in self.schedule.items():
            line = f"{k}\n{v}\n\n"
            text += line
        
        return text
    
if __name__ == "__main__":
    #testing
    
    program = trainingProgram() #create a training program. Eventually, I'll want a function to grab the input (name & training schedule names) from the user to customize this
    schedule = trainingSchedule() #create a training schedule. Same deal here, I'll want to customize this based on user input
    
    program.add_schedule(schedule) #add the schedule to the program
    print(program) #print the program to see the result of the mapping