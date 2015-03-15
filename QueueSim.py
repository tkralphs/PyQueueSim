'''
Basic M/M/s queueing module
Brief description:
Contains EventQueue class which can create an m/m/s queueing system instance,
and simulate with graphics

Detailed description:
Classes contained:
Event:
    Basically there are two event types, arrival and departure, this class
    can defines arrival and departure events
    attributes:
        number:                event number, each arrival/departure has a
                               unique event number, corresponding
                               arrival-departure pairs have the same event
                               number
                               type: int
        eventType:             either arrival or departure
                               arrival and departure are global constants
                               type: int
        eventTime:             occurance time of the event
                               type: float
        serverNumber:          server that serves the corresponding customer
                               of the event (arrival/departure)
                               type: int
        name:                  name of the event
                               type: string
    methods:
        __init__(self,eventType,number,eventTime,server=None):
                               constructor of the class
                               input descriptions are same as in the
                               attributes section, server input is optional
        __gt__(self,other):    returns True if self.eventTime > 
                               other.eventTime
        __ge__(self,other):    returns True if self.eventTime >= 
                               other.eventTime
        __lt__(self,other):    returns True if self.eventTime < 
                               other.eventTime
        __le__(self,other):    returns True if self.eventTime <= 
                               other.eventTime
        __eq__(self,other):    returns True if self.eventTime == 
                               other.eventTime
        __ne__(self,other):    returns True if self.eventTime != 
                               other.eventTime
Customer:
    A very basic class that defines customer types. It only has __init__()
    method that initializes attributes.
    attributes:
        entryTime:            arrival time of the customer
                              type: float
        serviceTime:          service time of the customer
                              type: float
        number                number of the customer
                              type: int
    methods:
        __init__(self,entryTime,serviceTime,customerNumber):
                              constructor of the class, inputs are as in the
                              attributes section 
EventQueue:
    This class holds the attributes and methods for the simulatio of M/M/s
    queueing system
    attributes:
        seed:                  seed used for random module
        IAT:                   mean of inter-arrival times between two
                               consecutive arrivals, inter-arrival times
                               are assumed to be exponentially distributed
                               type: float
        ST:                    mean of service time. Service times are
                               assumed to be exponentially distributed
                               type: float
        currentTime:            value that shows time
                               type: float
        server:                list that holds the status of the
                               servers, BUSY if busy, IDLE if not
                               type: list
        sqList                 list of queues, contains 1 queue if
                               queueing_mode == 'single', server_num queues 
                               if queueing_mode in ('random', 'shortest')
                               type: list
        eventTable:            list that holds the events, events are sorted
                               with respect to their occurance time
                               type: list
        waitingTime:           dictionary that holds the waiting times of the
                               customers in the queue, keys are customer 
                               numbers (Event numbers)
                               type: dict
        TIS:                   time spent in system for each customer,
                               it is dictionary type and keys are customer
                               numbers
                               type: dict
        serviceTime:           service time of the customer, dictionary type,
                               keys are customer numbers
                               type: dict
        eventCounter:          arrival event counter, increases by 1 with
                               each arrival
                               type: int
        customerCounter:       departure event counter, increases by 1 with
                               each departure
                               type: int
        queueing_mode:         determines the queue mode, set by set_mode()
                               if mode == 'single' there is single queue, 
                               if mode == 'random', then the number of queues 
                               equals the number of servers and new customers
                               join a random queue according to distribution
                               self.pi
                               if mode == 'shortest', then the number of queues 
                               equals the number of servers and new customers
                               join the shortest queue
                               type: string
        graphics_mode:         graphical mode, if graphics_mode == 'off', then
                               no graphics, graphics_mode == 'on', then
                               simulate with graphics
                               type: string
        server_num:            number of servers
        queue_num:             number of queues

    methods:
        __init__(self, seedInput, IAT, ST, pi, server_num,
                 queueing_mode, graphics_mode):
                               constructor of the class, seedInput is the
                               seed of simulation, IAT and ST are as in
                               attributes section
        set_mode(self, server_num, queueing_mode, graphics_mode):
                               server_num is a positive integer
                               queueing_mode is either 'single', 'random',
                               or 'shortest'
                               graphics_mode is either string 'off' or 
                               'on'
        which_queue(self):     when an arrival occurs this methods is called
                               if  there is an available server this method
                               returns to the tuple of (queue,server) where
                               queue represents the queue that the customer
                               should join and server is one of the available
                               servers
                               if there is no available server, server value
                               returned is None
        process_event(self,event):
                               processes event given and updates sqList and
                               eventTable accordingly 
        simulate(self, simulationLength):
                               simulates the system for simulationLength time
                               units
        print_stat(self):      print statistics to stdout
        add_event(self,event): adds event to the eventTable
        get_event(self,event): gets the first event in the event table
        draw_screen(self):     draws the status of the system to the screen
        display_init(self):    initializes pygame related parameters

Global Constants
Event Types
    ARRIVE = 0
    DEPART = 1
Server States
    IDLE = 0
    BUSY = 1

Created on Feb 9, 2012
Edited on Feb 11, 2013
'''

__version__    = '1.0.0'
__author__     = 'Aykut Bulut, Ted Ralphs (ayb211@lehigh.edu,ted@lehigh.edu)'
__license__    = 'MIT'
__maintainer__ = 'Aykut Bulut'
__email__      = 'ayb211@lehigh.edu'
__title__      = 'M/M/s queueing system'

from random import seed, expovariate
from math import sqrt, pow
import pygame
from pygame.locals import QUIT
from coinor.blimpy import Queue, PriorityQueue
from random import random

# Event Types
ARRIVE = 0
DEPART = 1
# Server States
IDLE = 0
BUSY = 1


class Event(object):
    '''
    Basically there are two event types, arrival and departure, this class can
    generate instances of arrival and departure events. See the file
    documentation for description of attributes.
    '''
    def __init__(self, eventType, eventNumber, eventTime, serverNumber = None):
        '''
        Constructor of the class. Input descriptions are same as in the
        module (up) documentation, server input is optional.
        '''
        self.number = eventNumber
        self.eventType = eventType
        self.eventTime = eventTime
        self.serverNumber = serverNumber
        if self.eventType == ARRIVE:
            self.name = 'arrival'+str(self.number)
        elif self.eventType == DEPART:
            self.name = 'departure'+str(self.number)
        else:
            print "unknown event type"

    def __gt__(self, other):
        '''
        Returns True if self.eventTime > other.eventTime
        '''
        return self.eventTime > other.eventTime

    def __ge__(self, other):
        '''
        Returns True if self.eventTime >= other.eventTime
        '''
        return self.eventTime >= other.eventTime

    def __lt__(self, other):
        '''
        Returns True if self.eventTime < other.eventTime
        '''
        return self.eventTime < other.eventTime

    def __le__(self, other):
        '''
        Returns True if self.eventTime <= other.eventTime
        '''
        return self.eventTime <= other.eventTime

    def __eq__(self, other):
        '''
        returns True if self.eventTime == other.eventTime
        '''
        return self.eventTime == other.eventTime

    def __ne__(self, other):
        '''
        Returns True if self.eventTime != other.eventTime
        '''
        return self.eventTime != other.eventTime

class Customer(object):
    '''
    Customer class. A basic class with only constructor method and 3
    attributes.
    '''
    def  __init__(self, entryTime, serviceTime, customerNumber):
        '''
        Initializes class attributes. See module documentation for explanation
        of attributes.
        '''
        self.entryTime = entryTime
        self.serviceTime = serviceTime
        self.number = customerNumber


class EventQueue(object):
    '''
    This class holds the attributes and methods for the simulation of M/M/s
    queueing system
    '''
    def __init__(self, seedInput = 0, IAT = 3, ST = 8, pi = None,
                 server_num = 3, queueing_mode = 'shortest',
                 graphics_mode = 'off'):
        '''
        Constructor of the class, sets initial values for class attributes
        Post: self.ii, self.seed, self.IAT, self.ST, self.currentTime,
        self.eventTable, self.waitingTime, self.TIS, self.serviceTime,
        self.eventCounter, self.customerCounter, self.server, self.sqList
        self.pi
        '''
        self.ii = 0
        seed(seedInput)
        self.seed = seedInput
        self.IAT = IAT
        self.ST = ST
        self.currentTime = 0.0
        self.eventTable = PriorityQueue()
        # waiting time of customers
        self.waitingTime = {}
        # time in system for each customer
        self.TIS = {}
        # service time for the corresponding customer
        self.serviceTime = {}
        self.eventCounter = 0
        self.customerCounter = 0
        self.set_mode(server_num, queueing_mode, graphics_mode)
        self.server = [IDLE for i in range(self.server_num)]
        self.sqList = [Queue() for i in range(self.queue_num)]
        # Equal probabilities by default
        if pi == None:
            pi = [1/float(self.queue_num) for i in range(self.queue_num)]
        #Ensure the probabilities sum to one
        pi[self.queue_num - 1] = 1 - sum(pi[:self.queue_num-1])
        self.pi = pi
        # Add first arrival event
        self.add_event(ARRIVE, self.currentTime)

    def set_mode(self, server_num = None, queueing_mode = None,
                 graphics_mode = None):
        '''
        server_num is a positive integer queueing_mode is either 'single',
        'random', or 'shortest' graphics_mode is either string 'off' or 'on'
        '''
        if queueing_mode:
            self.queueing_mode = queueing_mode
        if server_num:
            self.server_num = server_num
            if self.queueing_mode != 'single':
                self.queue_num = self.server_num
            else:
                self.queue_num = 1
        if graphics_mode:
            self.graphics_mode = graphics_mode
        if graphics_mode == 'on' and self.server_num > 50:
            print 'Only visualizing first 50 servers'

    def process_event(self, event):
        '''
        processes event given and updates sqList and eventTable accordingly
        '''
        if event.eventType == ARRIVE: 
            whichQueue, whichServer = self.which_queue()
            serviceTime = expovariate(1.0/self.ST)
            if whichServer == None:
                self.sqList[whichQueue].enqueue(Customer(self.currentTime, 
                                                         serviceTime, 
                                                         self.customerCounter))
            else:
                self.waitingTime[self.customerCounter] = 0
                self.serviceTime[self.customerCounter] = serviceTime
                self.add_event(DEPART, self.currentTime + serviceTime, 
                               whichServer)
            self.customerCounter += 1
            self.add_event(ARRIVE, self.currentTime+expovariate(1.0/self.IAT))
        elif event.eventType == DEPART:
            if self.queue_num == 1:
                q = self.sqList[0]
            else:
                q = self.sqList[event.serverNumber]
            if not q.isEmpty():
                customer = q.dequeue()
                self.waitingTime[customer.number] = (self.currentTime - 
                                                     customer.entryTime)
                self.serviceTime[customer.number] = customer.serviceTime
                self.add_event(DEPART, self.currentTime + customer.serviceTime,
                               event.serverNumber)
            else:
                self.server[event.serverNumber] = IDLE
        else:
            print "Unknown event type"
            
    def which_queue(self):
        '''
        When an arrival occurs this methods is called if  there is an available
        server this method returns to the tuple of (queue,server) where queue
        represents the queue that the customer should join and server is one of
        the available servers if there is no available server, server value
        returned is None
        '''
        # Single server policy
        if self.queueing_mode == 'single':
            if self.sqList[0].isEmpty():
                for i in range(self.server_num):
                    if self.server[i] == IDLE:
                        self.server[i] = BUSY
                        return 0, i
            else:
                return 0, None
            return 0, None
        # COMPLETE CHOOSING RANDOM QUEUE
        elif self.queueing_mode == 'random':
            pass
        # COMPLETE CHOOSING SHORTEST QUEUE
        elif self.queueing_mode == 'shortest':
            pass

    def simulate(self, simulationLength):
        '''
        Simulates the system for simulationLength time units
        '''
        pgEventType = None
        if self.graphics_mode == 'on':
            self.display_init()
        while self.currentTime < simulationLength and pgEventType != QUIT:
            if self.graphics_mode == 'on':
                for pgEvent in pygame.event.get():
                    pgEventType = pgEvent.type
                self.clock.tick(self.framerate)
                self.draw_screen()
                self.screen.blit(self.background, (0,0))
                pygame.display.flip()
            event = self.get_event()
            self.process_event(event)

    def print_stat(self):
        '''
        Print statistics to stdout.
        '''
        for k in self.waitingTime:
            self.TIS[k] = self.waitingTime[k] + self.serviceTime[k]
        n1 = len(self.waitingTime)
        n2 = len(self.serviceTime)
        n3 = len(self.TIS)
        av1 = sum(self.waitingTime.values())/n1
        av2 = sum(self.serviceTime.values())/n2
        av3 = sum(self.TIS.values())/n3
        stdev1 = sqrt(sum([pow(self.waitingTime[i]-av1,2) for i in self.waitingTime])/(n1-1))
        stdev2 = sqrt(sum([pow(self.serviceTime[i]-av2,2) for i in self.serviceTime])/(n2-1))
        stdev3 = sqrt(sum([pow(self.TIS[i]-av3,2) for i in self.TIS])/(n3-1))
        print '\n'
        print 'Seed: ', self.seed
        print 'Mode', self.queueing_mode
        print 'Simulation ended at ', self.currentTime
        print '=========================\t STATISTICS',
        print ' \t ========================='
        print '\t\t\tObservations\tAverage\t\tStDev'
        print 'Waiting Time\t\t', n1, '\t\t', av1, '\t', stdev1
        print 'Service Time\t\t', n2, '\t\t', av2, '\t', stdev2
        print 'Time is System\t\t', n3, '\t\t', av3, '\t', stdev3

    def add_event(self, eventType, eventTime, serverNumber = None):
        '''
        Adds event to the eventTable
        '''        
        self.eventCounter += 1
        self.eventTable.push(Event(eventType, self.eventCounter, 
                                   eventTime, serverNumber))

    def get_event(self):
        '''
        Gets the first event in the event table
        '''        
        e = self.eventTable.pop()
        self.currentTime = e.eventTime
        return e

    def draw_screen(self):
        '''
        Draws the status of the system to the screen
        '''        
        # Draw queue and server rectangles
        for i in range(min(self.server_num, 50)):
            pygame.draw.rect(self.background, self.colors[self.server[i]],
                             self.rec[i])
        # Draw customer rectangles
        if self.queueing_mode == 'single':
            nrInQ = self.sqList[0].size()
            for i in range(46):
                rect = (690-i*15,305,self.cDimension[0],self.cDimension[1])
                if i<nrInQ:
                    pygame.draw.rect(self.background,self.colors['c'],rect)
                else:
                    pygame.draw.rect(self.background,self.colors['bg'],rect)
        else:
            for j in range(min(self.server_num, 50)):
                nrInQ = self.sqList[j].size()
                for i in range(46):
                    rect = (690-i*15,self.server_position[j],
                            self.cDimension[0], self.cDimension[1])
                    if i<nrInQ:
                        pygame.draw.rect(self.background,self.colors['c'],rect)
                    else:
                        pygame.draw.rect(self.background,self.colors['bg'],rect)

    def display_init(self):
        '''
        Initializes pygame related parameters.
        '''        
        pygame.init()
        # pygame display parameters
        self.cDimension = (10, 10)
        self.sDimension = (10,10)
        server_spacing = 550/min(self.server_num, 50)
        padding = (600-(min(self.server_num, 50) - 1)*server_spacing)/2
        self.server_position = [padding + i*server_spacing 
                                for i in range(min(self.server_num, 50))]
        self.rec = [(740, self.server_position[i], self.sDimension[0],
                     self.sDimension[1])
                    for i in range(min(self.server_num, 50))]
        self.framerate = 100
        self.colors = {'bg':(0,0,0),
                       'c':(0,0,200),
                       False:(0,255,0),
                       True:(255,0,0)}
        # end of pygame display parameters
        self.screenDimension = (800,600) 
        self.screen = pygame.display.set_mode(self.screenDimension)
        pygame.display.set_caption(__title__)
        self.background = self.screen.convert()
        self.clock = pygame.time.Clock()


if __name__ == '__main__':
    length = 1000
    seedInput = 1
    server_num = 11
    IAT = 1
    ST = 11
    queueing_modes = ['single', 'shortest', 'random']
    pi_vecs = [None, [.5, .05, .05, .05, .05, .05, .05, .05, .05, .05, .05]]
    eq = EventQueue(seedInput = seedInput, IAT = IAT, ST = ST, pi = None, 
                    server_num = server_num, queueing_mode = 'single',
                    graphics_mode = 'off')
    #eq.simulate(length)
    #eq.print_stat()        
    
    for mode in queueing_modes:
        if mode == 'random':
            for pi in pi_vecs:
                eq = EventQueue(seedInput = seedInput, IAT = IAT, ST = ST, pi = pi, 
                                server_num = server_num, queueing_mode = mode, 
                                graphics_mode = 'off')
                eq.simulate(length)
                eq.print_stat()        
        else:
            eq = EventQueue(seedInput = seedInput, IAT = IAT, ST = ST, pi = None, 
                            server_num = server_num, queueing_mode = mode, 
                            graphics_mode = 'off')    
            eq.simulate(length)
            eq.print_stat()
