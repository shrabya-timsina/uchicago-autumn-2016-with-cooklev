# CS121: Polling places
#
# Name: Steven Cooklev and Shrabya Timsina
# Main file for polling place simulation

import sys
import util

from queue import PriorityQueue

def test_all():
    json = "data/config-3.json"
    num_booths = 1
    util.print_voters(simulate_election_day(json, num_booths))

### YOUR voter, voter_sample, and precinct classes GO HERE.
    
class Voter(object):
    """
    contains information about the voter 
    using info passed from Voter_Sample class
    """
    
    def __init__(self, gap_time, voting_duration, time_now):
        
        self._arrival_time = time_now + gap_time 
        self._voting_duration = voting_duration
        self._start_time = None 
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


    @start_time.setter
    def start_time(self, value_from_Vsample):
        self._start_time = value_from_Vsample

    @departure_time.setter
    def departure_time(self, value_from_Vsample):
        self._departure_time = value_from_Vsample

    def __str__(self):
        return "Voter({}, {}, {}, {})".format(self.arrival_time, 
            self.voting_duration, self.start_time, self.departure_time)

    def __repr__(self):
        return (str(self))



class Voter_Sample(object):
    """
    obtains gap and voting duration times
    creates voter instances and gives them start and depart times
    """
    
    def __init__(self, arrival_rate, voting_rate):
        
        #obtaining actual times by prviding rates
        (self.gap_time, self.voting_duration) = \
            util.gen_voter_parameters(arrival_rate, voting_rate)
        
    def __str__(self):
        return "Voter_Sampled({}, {})".format(self.gap_time, 
            self.voting_duration)    

    def __repr__(self):
         return str(self)   
    

    def has_next(self, time_now, total_time_in_min, num_voters_remaining):
        """
        checks to see if there are remaining valid voters
        and returns a boolean 
        """

        max_voter_condition = (num_voters_remaining > 0)
        time_condition = (time_now + self.gap_time <= total_time_in_min)
        all_conditions = max_voter_condition and time_condition
        
        return all_conditions


        
    ### GRADER COMMENT:
    ### Logic here should be placed inside simulate_election_day.
    ### Penalty: -3 Pts
    def next(self, booth_queue, time_now):
        """
        assigns a start time to a voter
        puts/removes a departure time from boothqueue
        """ 
        #creating an instance of a voter class 
        new_voter = Voter(self.gap_time, self.voting_duration, time_now)
        
        #voters start voting on arrival if a booth is empty
        if booth_queue.full() == False: 
            
            new_voter.start_time = new_voter.arrival_time
            new_voter.departure_time = new_voter.start_time + \
                new_voter.voting_duration
            
            booth_queue.put(new_voter.departure_time) 
        
        else:
            next_available_departure = booth_queue.get()
            
            #if the voter's arrival time is after the earliest depart time
            #then they vote upon arrival 
            if next_available_departure < new_voter.arrival_time: 
                new_voter.start_time = new_voter.arrival_time
            
            #if the voter's arrival time is before the earliest depart time
            #then they vote right after the earliest depart time
            else:
                new_voter.start_time = next_available_departure 
            
            new_voter.departure_time = new_voter.start_time + \
                new_voter.voting_duration
            booth_queue.put(new_voter.departure_time)
        
        return new_voter


class Precinct(object):
    """
    extracts information about precint from json file
    uses information to create a boothqueue and simulate election
    """

    ### GRADER COMMENT:
    ### Bugs here. json is not a file, it's already parsed. Modified by grader.
    ### Penalty: -1 Pts
    def __init__(self, json, num_booths):

        #prec_info = util.setup_config(json, num_booths)
        prec_info = json
        self.arrival_rate = prec_info["arrival_rate"]
        self.hours_open =  prec_info["hours_open"]
        self.max_time_in_min = 60 * self.hours_open
        self.num_voters = prec_info["num_voters"] 
        self.num_booths = num_booths
        self.seed = prec_info["seed"]
        self.voting_rate = prec_info["voting_duration_rate"]
       
    def __repr__(self):
        return ("arrival_rate is " + str(self.arrival_rate) + 
            ", hours_open are " + str(self.hours_open) +
            ", num_voters are " + str(self.num_voters) +
            ", seed: " + str(self.seed))        

    ### GRADER COMMENT: 
    ### You should not placed simulation logic inside this class. Those should be in simulate_election_day.
    ### Penalty: -3 Pts

    def simulate_election_in_precinct(self):
        """
        requests new voter generation while voters arrive before closing time
        and there are still voters remaining
        and adds voters who have voted to voter_list
        """

        voter_list = []
        time_now = 0
        num_voters_remaining = self.num_voters

        #stores the departure times of voters who are using the booths
        booth_queue = PriorityQueue(self.num_booths)

        if self.num_booths > 0 and self.num_voters > 0:
            generate_voter = Voter_Sample(self.arrival_rate, self.voting_rate)

            while generate_voter.has_next(time_now, self.max_time_in_min, 
                num_voters_remaining):
                
                next_voter = generate_voter.next(booth_queue, time_now)
                voter_list.append(next_voter)
                
                num_voters_remaining -= 1
                time_now = next_voter.arrival_time
                
                generate_voter = Voter_Sample(self.arrival_rate, 
                    self.voting_rate)

        return voter_list



### GRADER COMMENT:
### You should not change the para list of given functions. Modified by grader.
### Penalty: -1 Pts

#def simulate_election_day(json, num_booths):
def simulate_election_day(json):
    """
    simulates an election at one precint 

    parameters: json - a precint config json file with precint info
                num_booths - the number of booths in the precinct

    returns: voter_list - the list of valid voter instances
    """
    num_booths = json["number_of_booths"]
    precint_instance = Precinct(json, num_booths)

    #simulation actually in .simulate_election_in_precinct of Precint class
    voter_list = precint_instance.simulate_election_in_precinct()     

    return voter_list

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
