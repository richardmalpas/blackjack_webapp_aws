# blackjack_webapp

Access my AWS instance on: https://richardswebapp.com

Rules:

This is a simplified version of casino Blackjack.  The player and the dealer start with a hand of 2 cards.  The aim for the player is to finish with either a higher score than the dealer that is not above 21 or beat the dealers score with a non busted hand of 5 cards, a "5 Card Trick".  The player draws additional cards infront of the dealer and therefore has a higher chance of busting out first. The player can choose to "Hit" (draw another card) or "Stick" (declare that you don't want any further cards in this round).  If the player "Sticks" before the dealer does, the dealer may continue to draw further cards until either bust or has a higher score than the player. 



How the program works:

The program uses client side session variables to store the states of variable between get and post requests, the session variables are stored client side as a encrypted browswer cookie, the player objects are pickled to binary raw data before being stored as session variables and then unpickled at time of the next callback.