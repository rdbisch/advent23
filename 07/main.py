import sys
import functools
import itertools

cards = {"A":0, "K":1, "Q":2, "J": 3, "T": 4, "9":5, "8": 6, "7": 7, "6":8, "5":9, "4": 10, "3": 11, "2": 12 }
cards2 ={"A":0, "K":1, "Q":2, "J": 13, "T": 4, "9":5, "8": 6, "7": 7, "6":8, "5":9, "4": 10, "3": 11, "2": 12 }

# Similar to label Hand but if there are jokers will 
#  search through all combinations of cards replacing those jokers
#  for the best hand. 
def labelHandJoker(hand):
    ohand = str(hand)
    hand = sorted(hand, key = cards2.get)
    jokers = sum([1 for el in hand if el == 'J'])

    best_hand = None
    for p in itertools.combinations_with_replacement(cards2.keys(), jokers):
        for i in range(5 - jokers, 5):
            hand[i] = p[i - 5 + jokers]

        this_hand = labelHand(hand)
        #print(f"hand {hand} score {this_hand}")
        if best_hand is None or (this_hand < best) or (this_hand == best and comparator_assumed_equality(hand, best_hand) == 1):
            #print(f"new best! {hand}")
            best_hand = hand.copy()
            best = this_hand

    if best_hand is None:
        # No jokers
        best_hand = hand.copy()
        best = labelHand(best_hand)

    #print(f"with hand {ohand}, I think the best hand is {best_hand} with {jokers}")
    return best

_labelHand_memo  = None
def labelHand(hand):
    global _labelHand_memo
    if _labelHand_memo is None:
        _labelHand_memo = {}
    
    h1 = ''.join(hand)
    if h1 in _labelHand_memo:
        return _labelHand_memo[h1]
    
    hand = sorted(hand, key = cards.get)
    r = None

    if (hand[0] == hand[1] and hand[1] == hand[2] and hand[2] == hand[3] and hand[3] == hand[4]): r = 1
    elif (hand[0] == hand[1] and hand[1] == hand[2] and hand[2] == hand[3]): r=2
    elif (hand[1] == hand[2] and hand[2] == hand[3] and hand[3] == hand[4]): r=2
    elif hand[0] == hand[1] and hand[2] == hand[3] and hand[2] == hand[4]: r=3
    elif hand[0] == hand[1] and hand[2] == hand[0] and hand[3] == hand[4]: r=3
    elif hand[0] == hand[1] and hand[0] == hand[2]: r=4
    elif hand[1] == hand[2] and hand[1] == hand[3]: r=4
    elif hand[2] == hand[3] and hand[2] == hand[4]: r= 4
    elif hand[0] == hand[1] and (hand[2] == hand[3] or hand[3] == hand[4]): r= 5
    elif hand[1] == hand[2] and hand[3] == hand[4]: r=5
    elif hand[0] == hand[1] or hand[1] == hand[2] or hand[2] == hand[3] or hand[3] == hand[4]: r=6
    else: r=7

    _labelHand_memo[h1] = r
    _labelHand_memo[''.join(hand)] = r
    return r 

# Only compares the ranks of the cards, not the hand value
def comparator_assumed_equality(hand1, hand2):
    # Assumed that the hands are the same ranks and just apply card ranking
    i = 0
    while i < 5:
        c1 = cards2[hand1[i]]
        c2 = cards2[hand2[i]]
        if (c1 < c2): return 1
        elif (c1 > c2): return -1
        i = i + 1
    # hand1==hand2
    return 0

# hand1 > hand2 without jokers?
def comparator_nojoker(hand1, hand2):
    r1 = labelHand(hand1)
    r2 = labelHand(hand2)
    if (r1 < r2): return 1
    elif (r1 == r2):
        i = 0
        while i < 5:
            c1 = cards2[hand1[i]]
            c2 = cards2[hand2[i]]
            if (c1 < c2): return 1
            elif (c1 > c2): return -1
            i = i + 1
        # hand1==hand2
        return 0
    else:
        return -1

# hand1 > hand2 with jokers?
def comparator(hand1, hand2):
    o1 = hand1[0]
    o2 = hand2[0]
    r1 = labelHandJoker(hand1[0])
    r2 = labelHandJoker(hand2[0])
    
    if (r1 < r2): return 1
    elif (r1 == r2):
        i = 0
        while i < 5:
            c1 = cards2[hand1[0][i]]
            c2 = cards2[hand2[0][i]]
            if (c1 < c2): return 1
            elif (c1 > c2): return -1
            i = i + 1
        # hand1==hand2
        return 0
    else:
        return -1

# pretty print list    
def pplist(alist, n):
    r = ""
    n = min(len(alist) - 1, n)
    for i in range(n):
        r += str(alist[i]) + ", "
    r += " ..., "
    for i in range(n):
        r += str(alist[-n + i]) + ", "
    return r
    
if __name__ == "__main__":
    hand = []
    for line in sys.stdin:
        line = line.strip().split(' ')
        hand.append( (line[0], int(line[1])))

    print(pplist(hand, 10))
    newhand = list.sort(hand, key=functools.cmp_to_key(comparator))
    print(pplist(hand, 10))

    result = 0
    for i, (hand, wager) in enumerate(hand):
        result += (i + 1) * wager
    print(result)