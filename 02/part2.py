import sys

# Return true if the game seems to satisfy the bag requirements
def parseGame(alist):
    max_seen = { "blue": 0, "green": 0, "red": 0 }
    for adict in alist:
        for color in max_seen.keys():
            max_seen[color] = max( max_seen[color], adict.get(color, 0) )
    return max_seen
#
#Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
#Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
#Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
#Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
#Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green
if __name__ == "__main__":
    result = 0
    # Each time this loop, we are in a new game
    for line in sys.stdin:
        game_num = int(line.split(':')[0].split(' ')[-1])
        game_obs = line.split(':')[1].split(';')  # e.g.. [' 3 blue, 4 red', ' 1 red, 2 green, 6 blue', ' 2 green']
        game_obs_r = []
        for obs in game_obs:   # e.g 3 blue, 4 red
            rr = {}
            reveal = obs.split(',')
            for color_str in reveal:  # e.g 3 blue
                #print(color_str)
                num = int(color_str.strip().split(' ')[0])
                color = color_str.strip().split(' ')[1]
                rr[color] = num
            game_obs_r.append(rr)
        
        pg = parseGame(game_obs_r)
        result += pg['red'] * pg['blue'] * pg['green']
    
    print(result)