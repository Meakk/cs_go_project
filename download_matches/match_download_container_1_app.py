from Match_recuperation.Data_Parse import *
import sys

player_name = "Memetits"
map_select = "de_inferno"
premade = ["Rogoj1ne","GiM6","Furiyox"]
os.system("echo 'test 2' ")

player_name = os.getenv("PLAYER")
premade = os.getenv("PREMADE")
cmd="echo "+player_name+premade
os.system(cmd)

print(player_name, premade)
match_recuperation_dict_txt(api_key="38b28095-4ca6-48b6-aec5-748f507d5fcf",
                            player_id="57c4c556-3b8e-4695-bf55-122dde5040db", starting_item_position_call=0,
                            return_items_call=1 , map_select=map_select, nickname = player_name, premade = premade,replace = True )