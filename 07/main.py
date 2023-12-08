import sys
import functools

cards = {"A":0, "K":1, "Q":2, "J": 3, "T": 4, "9":5, "8": 6, "7": 7, "6":8, "5":9, "4": 10, "3": 11, "2": 12 }

def labelHand(hand):
    hand = sorted(hand, key = cards.get)
    if (hand[0] == hand[1] and hand[1] == hand[2] and hand[2] == hand[3] and hand[3] == hand[4]): return 1
    elif (hand[0] == hand[1] and hand[1] == hand[2] and hand[2] == hand[3]): return 2
    elif (hand[1] == hand[2] and hand[2] == hand[3] and hand[3] == hand[4]): return 2
    elif hand[0] == hand[1] and hand[2] == hand[3] and hand[2] == hand[4]: return 3
    elif hand[0] == hand[1] and hand[2] == hand[0] and hand[3] == hand[4]: return 3
    elif hand[0] == hand[1] and hand[0] == hand[2]: return 4
    elif hand[1] == hand[2] and hand[1] == hand[3]: return 4
    elif hand[2] == hand[3] and hand[2] == hand[4]: return 4
    elif hand[0] == hand[1] and (hand[2] == hand[3] or hand[3] == hand[4]): return 5
    elif hand[1] == hand[2] and hand[3] == hand[4]: return 5
    elif hand[0] == hand[1] or hand[1] == hand[2] or hand[2] == hand[3] or hand[3] == hand[4]: return 6
    else: return 7

# hand1 > hand2?
def comparator(hand1, hand2):
    r1 = labelHand(hand1[0])
    r2 = labelHand(hand2[0])
    if (r1 < r2): return 1
    elif (r1 == r2):
        i = 0
        while i < 5:
            c1 = cards[hand1[0][i]]
            c2 = cards[hand2[0][i]]
            if (c1 < c2): return 1
            elif (c1 > c2): return -1
            i = i + 1
        # hand1==hand2
        return 0
    else:
        return -1
    
if __name__ == "__main__":
    hand = []
    for line in sys.stdin:
        line = line.strip().split(' ')
        hand.append( (line[0], int(line[1])))

    print(hand[0], hand[1], hand[2], "...", hand[-3], hand[-2], hand[-1])
    newhand = list.sort(hand, key=functools.cmp_to_key(comparator))
    print(hand[0], hand[1], hand[2], "...", hand[-3], hand[-2], hand[-1])

    result = 0
    for i, (hand, wager) in enumerate(hand):
        result += (i + 1) * wager
    print(result)