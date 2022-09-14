from Match_recuperation.Data_Parse import *

list_match = read_all_csgo_match_of_one_map_json("de_overpass")
print(list_match[0])
print(list_match[1])