
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
    map_select = "de_inferno"
    premade = []

    match_recuperation_dict_txt(api_key="38b28095-4ca6-48b6-aec5-748f507d5fcf",
                                player_id="57c4c556-3b8e-4695-bf55-122dde5040db", starting_item_position_call=0,
                                return_items_call=40 , map_select=map_select, nickname = player_name, premade = premade,replace = True )
    
    list_match = read_all_csgo_match_of_one_map_json(map_select)
    
    print("TEZTSETDSF", len(list_match))
    
    print(fav_bomb_site_analysis(player_name,list_match,map_select))
    
    print("SIDE = T, map:",map_select,"team :",player_name)
    df = gunround_analysis(player_name,map_select,list_match,side = 't')
    
    print("SIDE = CT, map:",map_select,"team :",player_name)
    df = gunround_analysis(player_name,map_select,list_match,side = 'ct',frame = 7)
# %%
