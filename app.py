from flask import Flask
#from redis import Redis, RedisError
import os
import socket
from cs_go_analyse.oppenent_analysis import *
# Connect to Redis
#redis = Redis(host="redis", db=0, socket_connect_timeout=2, socket_timeout=2)

app = Flask(__name__)

@app.route("/")
def hello():
    player_name = "Memetits"
    map_select = "de_inferno"
    list_match = read_all_csgo_match_of_one_map_json(map_select)
    html = "<h3>Analyse de {nom}!</h3>" \
           "<b>Hostname:</b> {map}<br/>" \
           "<b>Visites:</b> {Team_info} <br/>" \
           "<p>Abonne toi!</p>"
    return html.format(nom=player_name, map=map_select, Team_info=fav_bomb_site_analysis(player_name,list_match,map_select))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)