# CS121: Polling places
#
# Steven and Shrabya
#
# Main file for polling place simulation

import sys
import util

from queue import PriorityQueue


def test_function(json, num_booths):
    t = 0
    voter_list = []
    prec = Precinct(json, num_booths)
    for voter in range(1, prec.num_voters):
        voter_sam = Voter_Sample(prec.arrival_rate, prec.voting_rate, t)
        t = voter_sam.arrival_time
        voter_list.append(voter_sam)
    print(voter_list)    
def test():
    prec1 = Precinct("data/config-0.json", 3)
    v1 = Voter_Sample(prec1.arrival_rate, prec1.voting_rate)

### YOUR voter, voter_sample, and precinct classes GO HERE.
    
class Voter(object):
    ID = 0
<<<<<<< HEAD
    def __init__(self, arrival_time, voting_duration):
        Voter.ID += 1
        self.ID = Voter.ID
        self.arrival_time = arrival_time
        self.voting_duration = voting_duration


    def __str__(self):
        return "Voter({}, {}, {})".format(self.ID, self.arrival_time, self.voting_duration)

    def __repr__(self):
        return (str(self))


class Voter_Sample(object):
    def __init__(self, arrival_rate, voting_rate, t):
        (self.gap_time, self.voting_duration) = util.gen_voter_parameters(arrival_rate, voting_rate)
        self.arrival_time = t + self.gap_time 
        self.start_time = None
        self.departure_time = None

    def __str__(self):
        return "Voter_Sampled({})".format(Voter(self.arrival_time, self.voting_duration))    

    def __repr__(self):
         return str(self)   


class Precinct(object):
    def __init__(self, json, num_booths):
        key = util.setup_config(json, num_booths)
        self.arrival_rate = key["arrival_rate"]
        self.hours_open = key["hours_open"]
        self.num_voters = key["num_voters"]
        self.num_booths = num_booths
        self.seed = key["seed"]
        self.voting_rate = key["voting_duration_rate"]
       
    def __repr__(self):
        return ("arrival_rate is " + str(self.arrival_rate) + 
            ", hours_open are " + str(self.hours_open) +
            ", num_voters are " + str(self.num_voters) +
            ", seed: " + str(self.seed))        

     
    def initialize_booths(self, num_booths):
        booth_queue = PriorityQueue(num_booths)
        return booth_queue

    def find_start_and_departure_of_next_voter(self, num_booths, booth_queue):
        if booth_queue.full() == False:
            next_voter = Voter_Sample(self.arrival_rate, self.voting_rate, t)
            next_voter.start_time = Voter_Sample.arrival_time
            next_voter.departure_time = next_voter.start_time + next_voter.voting_duration
            booth_queue.put(next_voter.start_time)
        else:
            value = booth_queue.get()
            booth_queue.put(value)
            next_voter.start_time = next_voter.arrival_time + value
            next_voter.departure_time = next_voter.start_time + next_voter.voting_duration
        return (next_voter.start_time, next_voter.departure_time)    


def simulate_election_day(json, num_booths):
    prec = Precinct(json, num_booths)
    booth_queue = initialize_booths(num_booths)
    
      
    # REPLACE [] with a list of voter objects
    return []
=======
    def __init__(self, json, num_booths):
        Voter.ID += 1
        self.ID =
        self.arrival_rate = arrival_rate
        self.voting_duration_rate = voting_duration_rate

    def __repr__(self):
        return ("arrival_time for voter is: " + str(self.arrival_time) +
            " departure_time:" + str(self.departure_time) +
            " Voter ID is" + str(self.ID))

    @property
    def arrival_time(self):
        self.gap = util.gen_voter_parameters(arrival_rate, voting_duration_rate)[0]
        prev_ID = self.ID - 1
        self.arrival_time = self.gap + arrival_time(self.prev_ID)
        return self.arrival_time


    @property
    def voting_duration(self):
        return util.gen_voter_parameters(arrival_rate, voting_duration_rate)[1]

    @property
    def departure_time(self):
        return (voting_duration(self) + start_time(self))


class Voter_Sample(object):
    ID = 0
    voter_list = []
    def __init__(self, json, num_booths):
        Precinct.__init__(self, json, num_booths)
        Voter.__init__(self, json, num_booths)
        while self.hours_open > 0:
            voter_info = (arrival_time(self), voting_duration(self), self.start_time, self.departure_time)
            voter_list.append(voter_info)
            self.hours_open = self.hours_open - arrival_time(self)
        print(voter_list)    

>>>>>>> 6d2992b61a054d601435b047992410ecb59af933


class Precinct(object):
    def __init__(self, json, num_booths):
        key = util.setup_config(json, num_booths)
        
        self.arrival_rate = key["arrival_rate"]
        self.hours_open = key["hours_open"]
        self.num_voters = key["num_voters"]
        self.num_booths = num_booths
        self.seed = key["seed"]
        self.voting_duration_rate = key["voting_duration_rate"]

    def __repr__(self):
        return ("arrival_rate is " + str(self.arrival_rate) +
            ", hours_open are " + str(self.hours_open) +
            ", num_voters are " + str(self.num_voters) +
            ", seed: " + str(self.seed))    



def simulate_election_day(config):
    # YOUR CODE HERE.
if __name__ == "__main__":
    # process arguments
    num_booths = 1

    if len(sys.argv) == 2:
        config_filename = sys.argv[1]
    elif len(sys.argv) == 3:
        config_filename = sys.argv[1]
        num_booths = int(sys.argv[2])
    else:
        s = "usage: python3 {0} <configuration filename>"
        s = s + " [number of voting booths]"
        s = s.format(sys.argv[0])
        print(s)
        sys.exit(0)

    config = util.setup_config(config_filename, num_booths)
    voters = simulate_election_day(config)
    util.print_voters(voters)
