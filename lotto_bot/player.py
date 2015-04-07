

class Player:
    def __init__(self):
        self.username = ""
        self.winnings  = 0
        self.user_id = ""            #the user's id number
        self.numbers = ""            #The convert list of the user's id

        self.messages = []           #contains sentences that tell on which days the user won something.

        self.match_four_dates = []
        
        self.three_correct = 0
        self.four_correct = 0
        self.five_correct = 0
        
        self.history_size = 0

        self.lost_number_message = ""

    def print_messages(self):
        print("hello worldd")

