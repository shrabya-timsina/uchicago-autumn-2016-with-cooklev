# CS121: Polling places
#
# Steven and Shrabya
#
# Main file for polling place simulation

import sys
import util

from queue import PriorityQueue

def test():
    Precinct("data/config-0.json", 3)
    Voter_Sample("data/config-0.json", 3)
    Voter("data/config-0.json", 3)

### YOUR voter, voter_sample, and precinct classes GO HERE.
        
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


class Voter(object):
    def __init__(self, json, num_booths):
        self.ID = ID
        ID += 1
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



def simulate_election_day(config):
    # YOUR CODE HERE.
    # REPLACE [] with a list of voter objects
    return []


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
