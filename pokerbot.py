from collections import Counter
from random import random

poker_hands_ranked = {
    "Royal Flush": 10,
    "Straight Flush": 9,
    "Four of a Kind": 8,
    "Full House": 7,
    "Flush": 6,
    "Straight": 5,
    "Three of a Kind": 4,
    "Two Pair": 3,
    "One Pair": 2,
    "High Card": 1
}

def evaluate_hand(hand, table_cards):
    # Placeholder for hand evaluation logic
    combined_cards = hand + table_cards
    mysuits = [card[1] for card in hand]
    myranks = [card[0] for card in hand]
    tablesuits = [card[1] for card in table_cards]
    tableranks = [card[0] for card in table_cards]

    if len(combined_cards) < 5:
        return 0  # Not enough cards to evaluate
    else:
        possibilities = []
        common_suits = set(mysuits) & set(tablesuits)
        common_ranks = set(myranks) & set(tableranks)
        for suit in common_suits:
            my_suit_cards = [card for card in hand if card[1] == suit]
            table_suit_cards = [card for card in table_cards if card[1] == suit]
            if len(my_suit_cards) + len(table_suit_cards) >= 5:
                possibilities.append({suit: 'Flush'})
                combined_ranks = [card[0] for card in my_suit_cards + table_suit_cards]
                if set(combined_ranks) >= set(['T', 'J', 'Q', 'K', 'A']):
                    possibilities.append({suit: 'Royal Flush'})
                for i in range(len(RANKS)- len(combined_ranks) + 1):
                    if set(RANKS[i:i+5]) <= set(combined_ranks):
                        possibilities.append({suit: 'Straight Flush'})

        for rank in common_ranks:
            my_rank_cards = [card for card in hand if card[0] == rank]
            table_rank_cards = [card for card in table_cards if card[0] == rank]
            if len(my_rank_cards) + len(table_rank_cards) == 4:
                possibilities.append({rank: 'Four of a Kind'})
            elif len(my_rank_cards) + len(table_rank_cards) == 3:
                possibilities.append({rank: 'Three of a Kind'})
            elif len(my_rank_cards) + len(table_rank_cards) == 2:
                possibilities.append({rank: 'One Pair'})

        # Create lists of keys that match the specific hand ranks
        threes = [cards for p in possibilities for cards, rank in p.items() if rank == 'Three of a Kind']
        pairs = [cards for p in possibilities for cards, rank in p.items() if rank == 'One Pair']

        # If both exist, we can form a Full House
        if threes and pairs:
            for t in threes:
                for p in pairs:
                    # Avoid using the same cards if they overlap (important for 5-card logic)
                    if t != p:
                        possibilities.append({f"{t} and {p}": 'Full House'})
        

        pair_cards = [cards for p in possibilities for cards, rank in p.items() if rank == 'One Pair']
        if len(pair_cards) >= 2:
            possibilities.append({f"{pair_cards[0]} and {pair_cards[1]}": 'Two Pair'})

        scores = []
        for p in possibilities:
            rank_name = list(p.values())[0]
            score = poker_hands_ranked[rank_name]
            scores.append(score)

        final_score = max(scores, default=1)
        
        print(f"Possibilities: {possibilities}")
        print(f"Final Score: {final_score}")
        
    return final_score 

def poker_bot_random_decision(hand,table_cards):
    score = evaluate_hand(hand, table_cards)
    if score >= 8:
        print("All-in")
    elif score >= 6:
        print("Raise")
    elif score >= 2:
        print("Call")
    else:
        print("Fold")

RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
RANK_DICT = {r:i for i,r in enumerate(RANKS)}
SUIT_MAP = {'h': 'hearts', 'd': 'diamonds', 'c': 'clubs', 's': 'spades'}
deck = [(r, s) for r in RANKS for s in SUIT_MAP.values()]

def remove_cards_from_deck(deck, cards_to_remove):
    return [card for card in deck if card not in cards_to_remove]

hand = []
flop = []
turn = []
river = []
# no_of_players = int(input("enter number of players: "))

for i in range(2):
    cardInput = input("enter your cards: ")
    r, s = cardInput[:-1].upper(), cardInput[-1].lower()
    hand.append((r, SUIT_MAP[s]))

def remove_cards_from_deck(deck, cards_to_remove):
    deck_copy = deck.copy()
    for card in cards_to_remove:
        if card in deck_copy:
            deck_copy.remove(card) 
    return deck_copy
    # return [card for card in deck if card not in cards_to_remove]

deck = remove_cards_from_deck(deck, hand)

for i in range(3):
    cardInput = input("enter flop cards: ")
    r, s = cardInput[:-1].upper(), cardInput[-1].lower()
    flop.append((r, SUIT_MAP[s]))

deck = remove_cards_from_deck(deck, flop)
poker_bot_random_decision(hand, flop)

cardInput = input("enter turn card: ")
r, s = cardInput[:-1].upper(), cardInput[-1].lower()
turn.append((r, SUIT_MAP[s]))

deck = remove_cards_from_deck(deck, turn)
poker_bot_random_decision(hand, flop+turn)

cardInput = input("enter river card: ")
r, s = cardInput[:-1].upper(), cardInput[-1].lower()
river.append((r, SUIT_MAP[s]))

deck = remove_cards_from_deck(deck, river)
poker_bot_random_decision(hand, flop+turn+river)
    
# print("Your Hand:", hand)
# print("Flop:", flop)
# print("Turn:", turn)
# print("River:", river)