import sys
import numpy as np

if __name__ == "__main__":
    result = 0
    
    copies = {}
    total = 0

    for line in sys.stdin:
        line = line.strip()
        tmp = line.split(':')
        card_num = int(tmp[0].split(' ')[-1])

        copies[card_num] = copies.get(card_num, 0) + 1
        total += copies[card_num]

        tmp2 = tmp[1].split('|')
        winners = set(tmp2[0].split(' '))
        numbers = set(tmp2[1].split(' '))
        if '' in winners: winners.remove('')
        if '' in numbers: numbers.remove('')
        inter = winners.intersection(numbers)
        print(f"{line} {winners} {numbers} {inter}")
        if len(inter) > 0:
            for new_card in range(card_num  + 1, card_num + 1 + len(inter)):
                copies[new_card] = copies.get(new_card, 0) + copies[card_num]

    print(total)