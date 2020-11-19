import simpy
import random

class Elevator(object):
    def __init__(self, env, current_state):
        self.frame = 0
        self.env = env
        self.current_state = current_state
        self.queues = [[], []]

        self.action = env.process(self.run())
        self.action = env.process(self.add_to_queue())
        
        self.emoji = None
        self.previous_state = None
    '''next_state selecteert de volgende state voor de lift'''
    
    def print_elevator(self):
        """This function Prints the elevator movements 
        """
        if self.previous_state not in [2,3]:
            if self.current_state == 2:
                self.emoji = self.queues[0].pop(0)
            elif self.current_state == 3:
                self.emoji = self.queues[1].pop(0)
            
        statenames = {0: ["│    │","│[  ]│"],
                      1: ["│[  ]│","│    │"], 
                      2: ["│    │",f"│[{self.emoji}]│"], 
                      3: [f"│[{self.emoji}]│","│    │"]}
        
        print(f"\n{self.frame:03d}:\n  ",
        f"{statenames[self.current_state][0]}",*self.queues[1],"\n   "
        f"{statenames[self.current_state][1]}", *self.queues[0])
        
        
    def next_state(self, current_state):
        """This function makes the elevator move and by changing its states.

        Args:
            current_state ([int]): [the current state the statemachine is in]
        """
        self.previous_state = current_state
        transition = "0"
        if current_state == 0 and len(self.queues[0]) > 0:
            transition = '1'
        elif current_state == 1 and len(self.queues[1]) > 0:
            transition = '1'
        elif current_state in [2,3] and self.previous_state in [1,2]:
            transition = '1'
        self.current_state = states[current_state][transition]
        self.frame+=1
    
    
    def run(self):
        duration = 4 #the elevotor takes 4 durations to move
        while True:
            self.print_elevator()
            self.next_state(self.current_state)
            yield self.env.timeout(duration)
    
   
    def add_to_queue(self, queue_duration=10):
        """ add_to_queue is a perallel progress which will increase the queue each 10 time steps"""
        emojis = "👩👨🧑👧🧓👴👦🧒👶🧔👲🤴👸"
        while True:
            self.queues[random.randrange(0,2)].append(random.choice(emojis))
            # print(self.queues)
            yield self.env.timeout(queue_duration)

'''states van de lift, states 0 t/m 3 zijn beschreven in de 'statenames' variabele'''
states = {0:{'0':1,'1':2}, 
          1:{'0':0,'1':3}, 
          2:{'0':0,'1':3}, 
          3:{'0':1,'1':2}}
# statenames = 
# statenames = {0: 'Floor 0 | Status: Free', 1: 'Floor 1 | Status: Free', 2: 'Floor 0 | Status: Occupied', 3: 'Floor 1 | Status: Occupied'}

env = simpy.Environment()
elevator = Elevator(env, 0)
env.run(until=100)
