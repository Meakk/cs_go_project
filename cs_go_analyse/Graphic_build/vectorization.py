import math


def coordonee_bomb_site(data):
    check_a = 0
    check_b = 0
    for r in range(len(data["gameRounds"])):
        if data["gameRounds"][r]["frames"][-1]["bombPlanted"]:
            if data["gameRounds"][r]["frames"][-1]["bombsite"] == "B":
                bomb = data["gameRounds"][r]["frames"][-1]["bomb"]
                coor_B = [bomb["x"], bomb["y"], bomb["z"]]
                check_b = 1
            if data["gameRounds"][r]["frames"][-1]["bombsite"] == "A":
                bomb = data["gameRounds"][r]["frames"][-1]["bomb"]
                coor_A = [bomb["x"], bomb["y"], bomb["z"]]
                check_a = 1
            if (check_a == 1) & (check_b == 1):
                break
    return coor_A, coor_B


def distance_point(vector1, vector2, map_select):
    if (map_select == "de_nuke") | (map_select == "de_overpass"):
        distance = math.sqrt((vector2[2] - vector1[2]) * (vector2[2] - vector1[2]))
    else:
        distance = math.sqrt(
            (vector2[0] - vector1[0]) * (vector2[0] - vector1[0])
            + (vector2[1] - vector1[1]) * (vector2[1] - vector1[1])
            + (vector2[2] - vector1[2]) * (vector2[2] - vector1[2])
        )
    return distance / 100
