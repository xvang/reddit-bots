



#This object stores all the players stats to be displayed.
#Taken from our great overlord ESPN.COM

class Player():

    def __init__(self, parent=None):
        self.dictionary = {}

        self.dictionary['name'] = "name"
        self.dictionary['link'] = "link"
        self.dictionary['gp'] = -1
        self.dictionary['gs'] = -1
        self.dictionary['min'] = -1
        self.dictionary['ppg'] = -1
        self.dictionary['offr'] = -1
        self.dictionary['defr'] = -1
        self.dictionary['rpg'] = -1
        self.dictionary['apg'] = -1
        self.dictionary['spg']  = -1
        self.dictionary['bpg'] = -1
        self.dictionary['tpg'] = -1
        self.dictionary['fpg'] = -1
        self.dictionary['ato'] = -1
        self.dictionary['per'] = -1
        

    #I couldn't think of a better way to input the values appropriately.
    #The inputting is in fetch_player_stats() in fetcher.py
    #The inputs should be in order, so I check in order.
    def brute_input(self, parsed_input):

        if (self.dictionary['name'] == "name"):
            self.dictionary['name'] = str(parsed_input)

        elif (self.dictionary['gp'] == -1):
            self.dictionary['gp'] = parsed_input
            
        
        elif (self.dictionary['gs'] == -1):
            self.dictionary['gs'] = parsed_input
            
            
        elif (self.dictionary['min'] == -1):
            self.dictionary['min'] = parsed_input
            
        elif (self.dictionary['ppg'] == -1):
            self.dictionary['ppg'] = parsed_input
            
        elif (self.dictionary['offr'] == -1):
            self.dictionary['offr'] = parsed_input
            
        elif (self.dictionary['defr'] == -1):
            self.dictionary['defr'] = parsed_input
            
        elif (self.dictionary['rpg'] == -1):
            self.dictionary['rpg'] = parsed_input
            
        elif (self.dictionary['apg'] == -1):
            self.dictionary['apg'] = parsed_input
            
        elif( self.dictionary['spg']  == -1):
            self.dictionary['spg'] = parsed_input
            
        elif (self.dictionary['bpg'] == -1):
            self.dictionary['bpg'] = parsed_input
            
        elif (self.dictionary['tpg'] == -1):
            self.dictionary['tpg'] = parsed_input
            
        elif (self.dictionary['fpg'] == -1):
            self.dictionary['fpg'] = parsed_input
            
        elif (self.dictionary['ato'] == -1):
            self.dictionary['ato'] = parsed_input
            
        elif (self.dictionary['per'] == -1):
            self.dictionary['per'] = parsed_input


    #The link fetched separately because it cannot be fetched the same way as the others.
    #without getting too complicated.
    def input_link(self, parsed_input):
        self.dictionary['link'] = str(parsed_input)

        
    def __str__(self):
        return self.dictionary['name']

        
