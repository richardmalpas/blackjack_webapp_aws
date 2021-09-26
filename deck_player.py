class Player():
    
    deck = []
    
    def __init__(self):
        self.player_hand = None


    def request_new_hand(self, size): #don't use!!!
        self.player_hand = []
        for item in range(size):
            self.new_card = Player.deck.pop(0)
            self.player_hand.append(self.new_card)

    def draw_new_card(self):
        self.new_card = Player.deck.pop(0)
        self.player_hand.append(self.new_card)
    
    
    def calculate_hand_strength(self, item):
        self.item = item + 1
        self.hand_strength = 0
        self.aces = 0
        for i in range(self.item):

            if self.player_hand[i][0] == "A":
                self.aces += 1
            elif self.player_hand[i][0] in {"J", "Q", "K"}:
                self.hand_strength += 10
            else:
                sum = self.player_hand[i][0]
                self.hand_strength += int(sum)
        
        for ace in range(self.aces):
            if (int(self.hand_strength) + 11 + (int(self.aces) - 1)) <= 21:
                self.hand_strength += 11
                continue
            self.hand_strength += 1
        if len(self.player_hand) == 5 and self.hand_strength <= 21:
            self.hand_strength = 100
            return str(self.hand_strength)
        return str(self.hand_strength)
    

if __name__ == '__main__':
    print("Please run app.py instead!")