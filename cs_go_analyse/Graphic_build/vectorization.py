import math

def coordonee_bomb_site(data):
    check_a = 0
    check_b = 0
    for r in range(len(data["gameRounds"])):
        try:
            for player in data["gameRounds"][r]["frames"][-1]['ct']['players']:
                if player["lastPlaceName"]=="BombsiteB":
                    coor_B= [player['x'],player['y']]
                    check_a=1
                if player["lastPlaceName"] == "BombsiteA":
                    coor_A = [player['x'], player['y']]
                    check_b=1
                if ((check_a == 1) & (check_b==1)):
                    break
        except:
            print("error coordonee_bomb_site")
    return coor_A,coor_B

def distance_point(vector1,vector2):
    distance = math.sqrt((vector2[0] - vector1[0]) * (vector2[0] - vector1[0])  + (vector2[1] - vector1[1])  * (vector2[1] - vector1[1]))
    return distance/100