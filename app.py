from flask import Flask
#from redis import Redis, RedisError
import os
import socket
from cs_go_analyse.oppenent_analysis import *
from download_matches.Match_recuperation.Data_Parse import *
#Connect to Redis
#redis = Redis(host="redis", db=0, socket_connect_timeout=2, socket_timeout=2)

app = Flask(__name__)
player_name = "Memetits"
map_select = "de_inferno"


@app.route("/")
def hello():
    list_match = read_all_csgo_match_of_one_map_json(map_select)
    df,data_player_t,data_grenade_t = gunround_analysis(player_name,map_select,list_match,side = 't')
    #df,data_player_ct,data_grenade_ct = gunround_analysis(player_name,map_select,list_match,side = 'ct')
    Team_info = fav_bomb_site_analysis(player_name,list_match,map_select)
    #df = gunround_analysis(player_name,map_select,list_match,side = 'ct',frame = 7)
    return f"<h3>Analyse du joueur Memetiti!</h3>" \
    f"<b>Map analyser:</b> {map_select}<br/>" \
    f"<b>Style de jeu:</b> {Team_info} <br/>" \
    f"<img src='data:image/png;base64,{data_player_t}'/>"\
    f"<img src='data:image/png;base64,{data_grenade_t}'/>"\
    #f"<img src='data:image/png;base64,{data_player_ct}'/>"\
    #f"<img src='data:image/png;base64,{data_grenade_ct}'/>"\
    #f"<p>More info à venir</p>"

@app.route("/download")
def test():
    
    player_name = "Memetits"
    map_select = "de_inferno"
    premade = ["Rogoj1ne","GiM6","Furiyox"]
    print(player_name,map_select)
    match_recuperation_dict_txt(api_key="38b28095-4ca6-48b6-aec5-748f507d5fcf",
                            player_id="57c4c556-3b8e-4695-bf55-122dde5040db", starting_item_position_call=0,
                            return_items_call=1 , map_select=map_select, nickname = player_name, premade = premade,replace = True )
    
    return f"<h3>Analyse du joueur Memetiti!</h3>" \
    f"<b>Map analyser:</b> {map_select}<br/>" \

    

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)