
#%%
from cs_go_analyse.oppenent_analysis import *
import pandas as pd
import time
import multiprocessing
from download_matches.Match_recuperation.Data_Parse import *
from cs_go_analyse.oppenent_analysis import *
import pandas as pd

if __name__ == "__main__":
    player_name = "Memetits"
    map_select = "de_nuke"
    premade = []

    match_recuperation_dict_txt(api_key="38b28095-4ca6-48b6-aec5-748f507d5fcf",
                                player_id="57c4c556-3b8e-4695-bf55-122dde5040db", starting_item_position_call=0,
                                return_items_call=50 , map_select=map_select, nickname = player_name, premade = premade,replace = True,
                                nb_match_analyses_max = 8)
    
    list_match = read_all_csgo_match_of_one_map_json(map_select)
# %%
