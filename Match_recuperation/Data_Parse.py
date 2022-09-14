import matplotlib.pyplot as plt
import imageio
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from awpy.parser import DemoParser
from sklearn.datasets import make_blobs
import math
import seaborn as sns
from faceit_api.faceit_data import FaceitData
import requests
import re
import ast
import zipfile
import patoolib
import os
import time
time.sleep(2)

def get_player_id(api_key="38b28095-4ca6-48b6-aec5-748f507d5fcf",nickname = "memetiti"):
    faceit_data = FaceitData(api_key)
    player_id = faceit_data.player_details(nickname=nickname)
    return player_id

def match_recuperation_dict_txt(api_key="38b28095-4ca6-48b6-aec5-748f507d5fcf",
                                player_id="57c4c556-3b8e-4695-bf55-122dde5040db", starting_item_position_call=0,
                                return_items_call=2,nickname = "memetiti", map_select = None):
    if nickname != "memetiti":
        player_id = get_player_id(nickname = nickname)['player_id']
        print(nickname," : ",player_id)
    faceit_data = FaceitData(api_key)
    all_match_player = faceit_data.player_matches(player_id=player_id, game="csgo",
                                                  starting_item_position=starting_item_position_call,
                                                  return_items=return_items_call)
    list_of_match = []
    succeed = 0
    cpt=0
    for i in range(len(all_match_player["items"])):
       cpt+=1
       try:
            carte =faceit_data.match_details(match_id=all_match_player["items"][i]['match_id'])['voting']['map']['pick'][0]
            print("_______________START DOWNLOADING MATCH NUMBER :",cpt, 'on map :', carte, "___SUCCEED BEFORE : ", succeed)
            if (map_select != None) & (carte != map_select) :
                print("wrong map: ",carte,"vs", map_select)
                continue
            verif = 0
            faceit_data = FaceitData("38b28095-4ca6-48b6-aec5-748f507d5fcf")
            print(all_match_player["items"][i]["match_id"])
            match_details = faceit_data.match_details(all_match_player["items"][i]["match_id"])
            match_name = all_match_player["items"][i]["match_id"]
            for root, dirs, files in os.walk("C:/demo_csgo/DataBase/" + match_details["voting"]["map"]["pick"][0]):
                for filename in files:
                    print(filename," compare to : ",nickname + "_" +  match_details["voting"]["map"]["pick"][0]+"_"+str(match_details["configured_at"])+"_"+match_name+'.txt')
                    if filename == nickname + "_" + match_details["voting"]["map"]["pick"][0] + "_" + str(
                            match_details["configured_at"]) + "_" + match_name + '.json':
                        verif = 1
                        break
            if verif == 1:
                print("demo déjà présente, on passe à la suite")
                continue
            url = match_details["demo_url"][0]
            headers = {
                'accept': 'application/json',
                'Authorization': 'Bearer {}'.format(api_key)
            }
            print(url)
            r = requests.get(url)
            #  print(r.status_code)
            with open('C:/demo_csgo/DataBase/' + match_details["voting"]["map"]["pick"][0] + "_" + str(
                    match_details["configured_at"]) + '.dem.7z', 'wb') as f:
                f.write(r.content)
            # print('C:/demo_csgo/DataBase/'+match_details["voting"]["map"]["pick"][0]+"_"+str(match_details["configured_at"])+'.dem.7z')
            print('C:/demo_csgo/DataBase/' + match_details["voting"]["map"]["pick"][0] + "_" + str(
                match_details["configured_at"]) + '.dem.7z')
            patoolib.extract_archive('C:/demo_csgo/DataBase/' + match_details["voting"]["map"]["pick"][0] + "_" + str(
                match_details["configured_at"]) + '.dem.7z', outdir="C:/demo_csgo/DataBase")
            s = match_details["demo_url"][0]
            pattern = "csgo/(.*?).dem"
            match_name = re.search(pattern, s).group(1)

            print("debut du parse")
            demo_parser = DemoParser(demofile='C:/demo_csgo/DataBase/' + match_name + '.dem',
                                     demo_id=str(match_details["configured_at"]), parse_rate=128)
            data = demo_parser.parse()
            print("parse success")

            os.remove('C:/demo_csgo/DataBase/' + match_name + '.dem')
            os.remove('C:/demo_csgo/DataBase/' + match_details["voting"]["map"]["pick"][0] + "_" + str(
                match_details["configured_at"]) + '.dem.7z')
            os.remove(str(match_details["configured_at"]) + ".json")
            match_name = all_match_player["items"][i]["match_id"]

            with open('C:/demo_csgo/DataBase/' + match_details["voting"]["map"]["pick"][0] + '/' + nickname + "_" +
                      match_details["voting"]["map"]["pick"][0] + "_" + str(
                    match_details["configured_at"]) + "_" + match_name + '.json', 'w') as json_file:
                json.dump(data, json_file)
            print(match_details["voting"]["map"]["pick"][0]+"_"+str(match_details["configured_at"])+"_"+match_name)
            succeed += 1
       except:
            print("error, try next : ",r.status_code)
            os.remove('C:/demo_csgo/DataBase/'+match_details["voting"]["map"]["pick"][0]+"_"+str(match_details["configured_at"])+'.dem.7z')
            os.system('clear')

def read_all_csgo_match_of_one_map_json(map_wanted):
    list_match=[]
    for root, dirs, files in os.walk("C:/demo_csgo/DataBase/"+map_wanted):
        for filename in files:
            pattern = "(.*?).json"
            filename = re.search(pattern, filename).group(1)
           # print(filename)
            with open("C:/demo_csgo/DataBase/"+map_wanted+"/"+filename+".json") as file:
                data=json.load(file)
                list_match.append(data)
    return list_match