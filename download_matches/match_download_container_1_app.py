import pandas as pd
import time
import multiprocessing
from Match_recuperation.Data_Parse import *
import pandas as pd
import warnings


from flask import Flask
app = Flask(__name__)

if __name__ == "__main__":
    warnings.filterwarnings('ignore')
    player_name = "Memetits"
    map_select = "de_overpass"
    premade = []

    match_recuperation_dict_txt(api_key="38b28095-4ca6-48b6-aec5-748f507d5fcf",
                                player_id="57c4c556-3b8e-4695-bf55-122dde5040db", starting_item_position_call=0,
                                return_items_call=10 , map_select=map_select, nickname = player_name, premade = premade,replace = True,
                                nb_match_analyses_max = 8)
    
@app.route("/")
def hello():
    
    #df = gunround_analysis(player_name,map_select,list_match,side = 'ct',frame = 7)
    return f"<h3>Analyse du joueur GiM6!</h3>" 
    #f"<img src='data:image/png;base64,{data_player_ct}'/>"\
    #f"<img src='data:image/png;base64,{data_grenade_ct}'/>"\
    #f"<p>More info à venir</p>"


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)

