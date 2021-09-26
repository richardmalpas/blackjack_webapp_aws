from flask import Flask, render_template, request, session, url_for
import deck_player
import pickle
import random

application = Flask(__name__)
application.secret_key = "sflefjdwlijqssfflcbscladcqqnzld"

@application.route('/', methods=['GET', 'POST'])
def main():

    try:
        if int(session['item']) >4:  # i don't think i need the int() ?       
            session['item'] = 0
    except KeyError:
        session['item'] = 0


    if request.method == 'GET' or (request.method == 'POST' and int(session['item']) == 0) or (request.method == 'POST' and request.form.get('start_new_game') or (request.method == 'POST' and session['game_over'] == True)): # If we are at the start of the game, remove all data from session
        for s in list(session):
            del session[s]

        dealer = deck_player.Player()
        new_player = deck_player.Player()
        suits = ["H", "D", "S", "C"]
        cards = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
     
        start_deck = []
        for suit in suits:
            for card in cards:
                start_deck.append([card, suit])
        random.shuffle(start_deck)
        deck_player.Player.deck = start_deck
        new_player.request_new_hand(2)
        dealer.request_new_hand(2)
        session['pickled_dealer'] = pickle.dumps(dealer)                           # Pickle all objects so that they are available for future POST request callbacks
        session['pickled_new_player'] = pickle.dumps(new_player)
        session['item'] = 0 # Reinstate session[item] after removing all data from the session object
        session['next_move_text'] = ""
        session['player_hand_value'] = 0
        session['dealer_hand_value'] = 0
        session['player_hand_concatinated_list'] = []
        session['dealer_hand_concatinated_list'] = []
        session['game_over'] = False
        session['player_draw'] = True
        session['dealer_draw'] = True


    #if request.method == 'POST' and int(session['item'] > 0):                   
    else:  # method is POST and itteration is > 0                               # Unpickle objects if current itteration is a later stage POST request callback
        dealer = pickle.loads(session['pickled_dealer'])
        new_player = pickle.loads(session['pickled_new_player'])
        session['item'] += 1   
        
        if request.form.get('hit'):
        
            if session['player_draw'] == True:
                new_player.draw_new_card()
            if (int(session['dealer_hand_value']) < 17 and session['player_draw'] == True and session['dealer_draw'] == True and int(session['dealer_hand_value']) < int(session['player_hand_value'])) or (int(session['dealer_hand_value']) < int(session['player_hand_value']) and session['dealer_draw'] == True):
                dealer.draw_new_card()
            elif session['player_draw'] == False:
                select_winner(str(session['dealer_hand_value']), str(session['player_hand_value']))
            else:
                session['dealer_draw'] = False

        else: # (Stick)
            session['player_draw'] = False
            if (int(session['dealer_hand_value']) < int(session['player_hand_value'])) and (session['dealer_draw'] == True):
                session['next_move_text'] = "\nPress 'Hit' to see dealers next move"
                dealer.draw_new_card()
            else:
                select_winner(str(session['dealer_hand_value']), str(session['player_hand_value']))

        
    for i in range(2): #Loops through twice if first itteration otherwise once using break
        if session['dealer_draw'] == True:
            try:
                session['dealer_hand_value'] = dealer.calculate_hand_strength(session['item'])
                session['dealer_hand_concatinated_list'].append(concatinate_cards(dealer.player_hand[session['item']])) 
            except IndexError:
                print("IndexError line 77")
            # (below) create a list of concatinated cards (suits and rank) to use to select svg card images in front end           
        
        if session['player_draw'] == True:
            session['player_hand_value'] = new_player.calculate_hand_strength(session['item'])
            # (below) create a list of concatinated cards (suits and rank) to use to select svg card images in front end           
            session['player_hand_concatinated_list'].append(concatinate_cards(new_player.player_hand[session['item']])) 
            

        if session['item'] == 0: # first itteration needs to run through the loop twice as 2 cards a drawn to start, this makes sure the correct text is displayed for cards 1 and 2 drawn.
            session['item'] += 1
            continue
        elif session['item'] == 1: # second itteration, render template and wait for next user input
            return render_template('game.html', item=session['item'], next_move_text=session['next_move_text'], dealer_hand=session['dealer_hand_concatinated_list'], dealer_hand_value=session['dealer_hand_value'], player_hand=session['player_hand_concatinated_list'], player_hand_value=session['player_hand_value'])    
        else:               
            break
    
   
    if int(session['player_hand_value']) > 21 and int(session['player_hand_value']) < 100:      # ? did the player bust
        session['player_hand_value'] = "0"
        select_winner(str(session['dealer_hand_value']), str(session['player_hand_value']))

    elif session['player_hand_value'] == "100":                                                 # ? did the player make a 5 card trick
        session['next_move_text'] = "You have a 5 Card Trick !!!"
        select_winner(str(session['dealer_hand_value']), str(session['player_hand_value']))


    if int(session['dealer_hand_value']) > 21 and int(session['dealer_hand_value']) < 100:      # ? did the dealer bust
        session['dealer_hand_value'] = "0"
        session['next_move_text'] = "Dealer Has Bust"
        select_winner(str(session['dealer_hand_value']), str(session['player_hand_value']))
    elif session['dealer_hand_value'] == "100":
        session['next_move_text'] = "Dealer has a 5 Card Trick !!!"
        select_winner(str(session['dealer_hand_value']), str(session['player_hand_value']))


    if session['item'] <= 4:                            # If theres another round,
        session['pickled_dealer'] = pickle.dumps(dealer)                    # Pickle all objects so that they are available for the next round POST request callback
        session['pickled_new_player'] = pickle.dumps(new_player)
        return render_template('game.html', item=session['item'], next_move_text=session['next_move_text'], dealer_hand=session['dealer_hand_concatinated_list'], dealer_hand_value=session['dealer_hand_value'], player_hand=session['player_hand_concatinated_list'], player_hand_value=session['player_hand_value'])

    else:
        select_winner(session['dealer_hand_value'], session['player_hand_value'])




def select_winner(dealer_score, player_score): # Winner is chosen
    session['game_over'] = True
    if int(player_score) > int(dealer_score):
        session['next_move_text'] = "You won !!!"
        
        return render_template('game.html', item=session['item'], next_move_text=session['next_move_text'], dealer_hand=session['dealer_hand_concatinated_list'], dealer_hand_value=session['dealer_hand_value'], player_hand=session['player_hand_concatinated_list'], player_hand_value=session['player_hand_value'])
    session['next_move_text'] = "You Lost !!!"
    return render_template('game.html', item=session['item'], next_move_text=session['next_move_text'], dealer_hand=session['dealer_hand_concatinated_list'], dealer_hand_value=session['dealer_hand_value'], player_hand=session['player_hand_concatinated_list'], player_hand_value=session['player_hand_value'])



def concatinate_cards(player_hand_list):
    concatinated_list = ''.join(player_hand_list)
    return concatinated_list






if __name__ == "__main__":
    #application.run(debug=False)
    application.run(host="0.0.0.0", port="80", debug=False)