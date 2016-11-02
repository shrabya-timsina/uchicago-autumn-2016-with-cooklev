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
    util.print_voters(voter_list)

def test_class():
    prec1 = Precinct("data/config-2.json", 2)
    v1 = Voter_Sample(prec1.arrival_rate, prec1.voting_rate, t = 0)
    print(prec1)
    print(v1)
    Precinct.find_start_and_dep_time_of_next_voter(prec1, 2, Precinct.initialize_booth(prec1, 2))


def test_all():
    json = "data/config-1.json"
    num_booths = 1
    simulate_election_day(json, num_booths)
    open("output.txt", 'w' )


### YOUR voter, voter_sample, and precinct classes GO HERE.
    
class Voter(object):
    
    def __init__(self, gap_time, voting_duration, t):
        
        self._voting_duration = voting_duration
        self._start_time = None
        self._arrival_time = t + gap_time 
        self._departure_time = None

    @property
    def arrival_time(self):
        return self._arrival_time

    @property
    def voting_duration(self):
        return self._voting_duration 

    @property
    def start_time(self):
        return self._start_time

    @property
    def departure_time(self):
        return self._departure_time

#delete later
    @arrival_time.setter
    def arrival_time(self, value_from_Vsample):
        self._arrival_time = value_from_Vsample ###

    @start_time.setter
    def start_time(self, value_from_Vsample):
        self._start_time = value_from_Vsample

    @departure_time.setter
    def departure_time(self, value_from_Vsample):
        self._departure_time = value_from_Vsample

    def __str__(self):
        return "Voter({}, {}, {}, {})".format(self.arrival_time, self.voting_duration, self.start_time, self.departure_time)

    def __repr__(self):
        return (str(self))



class Voter_Sample(object):
    def __init__(self, arrival_rate, voting_rate):
        self.arrival_rate = arrival_rate
        self.voting_rate = voting_rate
         

    def __str__(self):
        return "Voter_Sampled({})".format(Voter(new_voter.arrival_time, new_voter.voting_duration, new_voter.start_time, new_voter.departure_time))    

    def __repr__(self):
         return str(self)   

    def find_start_and_dep_time(self, booth_queue, t):
        
        (gap_time, voting_duration) = util.gen_voter_parameters(self.arrival_rate, self.voting_rate)
        new_voter = Voter(gap_time, voting_duration, t)

        if booth_queue.full() == False:
            new_voter.start_time = new_voter.arrival_time
            new_voter.departure_time = new_voter.start_time + new_voter.voting_duration
            booth_queue.put(new_voter.departure_time)
        else:
            next_available_departure = booth_queue.get()
            if next_available_departure < new_voter.arrival_time:
                new_voter.start_time = new_voter.arrival_time
            else:
                new_voter.start_time = next_available_departure 
            new_voter.departure_time = new_voter.start_time + new_voter.voting_duration
            booth_queue.put(new_voter.departure_time)
        return new_voter


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

     
    def initialize_booth(self, num_booths):
        booth_queue = PriorityQueue(num_booths)
        return booth_queue


def simulate_election_day(json, num_booths):
    voter_list = []
    t = 0
    prec = Precinct(json, num_booths)
    total_time_in_min = 60 * prec.hours_open
    num_voters_remaining = prec.num_voters
    booth_queue = prec.initialize_booth(num_booths)

    generate_voter = Voter_Sample(prec.arrival_rate, prec.voting_rate)
    #print(generate_voter)
    new_voter = generate_voter.find_start_and_dep_time(booth_queue, t)
    t = new_voter.arrival_time

    #print(new_voter)

    while new_voter.arrival_time < total_time_in_min and num_voters_remaining > 0:
        voter_list.append(new_voter)
        num_voters_remaining -= 1
        oldvoter = new_voter.departure_time
        generate_voter = Voter_Sample(prec.arrival_rate, prec.voting_rate)
        #print(generate_voter)
        new_voter = generate_voter.find_start_and_dep_time(booth_queue, t)
        new_voter.arrival_time = oldvoter
        t = new_voter.arrival_time

    return util.print_voters(voter_list)

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
