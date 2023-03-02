from cs_go_analyse.oppenent_analysis import *
import pandas as pd
import time
import multiprocessing

if __name__ == "__main__":
    start = time.time()
    player_name = "Memetits"
    map_select = "de_inferno"
    list_match = read_all_csgo_match_of_one_map_json("de_inferno")
    
    tests = multiprocessing.Process(target=fav_bomb_site_analysis, args=(player_name,list_match,map_select ))
    tests.start()
    proc2 = multiprocessing.Process(target=gunround_analysis, args=(player_name,map_select,list_match,'t',7))
    proc2.start()

    end = time.time()
    print("Time spent :",end - start,"s")