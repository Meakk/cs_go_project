import json
import os
from awpy.parser import DemoParser
from .faceit_api.faceit_data import FaceitData
import requests
import re
import patoolib
import multiprocessing

import time
time.sleep(2)

def get_player_id(api_key="38b28095-4ca6-48b6-aec5-748f507d5fcf",nickname = "memetiti"):
    os.system("echo 'before api key'")
    faceit_data = FaceitData(api_key)
    os.system("echo 'after api key'")
    player_id = faceit_data.player_details(nickname=nickname)
    return player_id

def match_recuperation_dict_txt(api_key="38b28095-4ca6-48b6-aec5-748f507d5fcf",
                                player_id="57c4c556-3b8e-4695-bf55-122dde5040db", starting_item_position_call=0,
                                return_items_call=2,nickname = "memetiti", map_select = None, premade=[],replace = False, nb_match_analyses_max = 4):
    os.system("echo 'first request'")
    if nickname != "memetiti":
        player_id = get_player_id(nickname = nickname)['player_id']
        print(nickname," : ",player_id)
    os.system("echo 'start download'")
    faceit_data = FaceitData(api_key)
    all_match_player = faceit_data.player_matches(player_id=player_id, game="csgo",
                                                  starting_item_position=starting_item_position_call,
                                                  return_items=return_items_call)
    list_of_match = []
    proc = []
    succeed = 0
    cpt=0
    if replace :
        filelist = [f for f in os.listdir('demo_csgo/DataBase/' + map_select)]
        for f in filelist:
            os.remove(os.path.join('demo_csgo/DataBase/' + map_select, f))
        print("##ALL file removed in ", 'demo_csgo/DataBase/' + map_select, "###")
    for i in range(len(all_match_player["items"])):
            cpt+=1
     #  try:
            match_detail = faceit_data.match_details(match_id=all_match_player["items"][i]['match_id'])
            carte = match_detail['voting']['map']['pick'][0]
            print("_______________START DOWNLOADING MATCH NUMBER :",cpt, 'on map :', carte, "___SUCCEED BEFORE : ", succeed)
            if (map_select != None) & (carte != map_select) :
                print("wrong map: ",carte,"vs", map_select)
                continue

            cpt = 0
            nb_premade = len(premade)
            print("Check premade : ")
            for faction in ['faction1','faction2']:
                for roster in match_detail['teams'][faction]['roster']:
                    if (roster['nickname'] in premade):
                        print(roster['nickname']," founded")
                        cpt += 1
            if cpt != nb_premade:
                print("###il manque :", nb_premade - cpt, " premade###")
                continue

            verif = 0
            faceit_data = FaceitData("38b28095-4ca6-48b6-aec5-748f507d5fcf")
            print(all_match_player["items"][i]["match_id"])
            match_details = faceit_data.match_details(all_match_player["items"][i]["match_id"])
            match_name = all_match_player["items"][i]["match_id"]
            
            for root, dirs, files in os.walk("demo_csgo/DataBase/" + match_details["voting"]["map"]["pick"][0]):
                for filename in files:
                    
                    print(filename," compare to : ",nickname + "_" +  match_details["voting"]["map"]["pick"][0]+"_"+str(match_details["configured_at"])+"_"+match_name+'.txt')
                    if filename == nickname + "_" + match_details["voting"]["map"]["pick"][0] + "_" + str(
                            match_details["configured_at"]) + "_" + match_name + '.json':
                        verif = 1
                        break
            print("nb_game_json:", succeed)
            
            if verif == 1:
                print("demo déjà présente, on passe à la suite")
                continue
            
            
            
            url = match_details["demo_url"][0]
            headers = {
                'accept': 'application/json',
                'Authorization': 'Bearer {}'.format(api_key)
            }
            
            proc.append(multiprocessing.Process(target=download_parse, args=(url,match_details,all_match_player,nickname,i )))
            succeed += 1
            if succeed >= nb_match_analyses_max:
                print("Enough matches downloaded")
                break
  
     #  except:
      #      print("error before download and parse")
    for proc1 in proc :
        proc1.start()
    print("En attente de FIN download and parse")
    for proc1 in proc :
        proc1.join()
    print("DONE Doawnloading and parsing")


            
            
            
def download_parse(url,match_details,all_match_player,nickname,i):
    try:
        print(url)
        r = requests.get(url)
        #  print(r.status_code)
        with open('demo_csgo/DataBase/' + match_details["voting"]["map"]["pick"][0] + "_" + str(
                match_details["configured_at"]) + '.dem.7z', 'wb') as f:
            f.write(r.content)
        # print('demo_csgo/DataBase/'+match_details["voting"]["map"]["pick"][0]+"_"+str(match_details["configured_at"])+'.dem.7z')
        print('demo_csgo/DataBase/' + match_details["voting"]["map"]["pick"][0] + "_" + str(
            match_details["configured_at"]) + '.dem.7z')
        patoolib.extract_archive('demo_csgo/DataBase/' + match_details["voting"]["map"]["pick"][0] + "_" + str(
            match_details["configured_at"]) + '.dem.7z', outdir="demo_csgo/DataBase")
        s = match_details["demo_url"][0]
        pattern = "csgo/(.*?).dem"
        match_name = re.search(pattern, s).group(1)

        print("debut du parse",'demo_csgo/DataBase/' + match_details["voting"]["map"]["pick"][0] + "_" + str(
            match_details["configured_at"]) + '.dem')
        demo_parser = DemoParser(demofile='demo_csgo/DataBase/' + match_details["voting"]["map"]["pick"][0] + "_" + str(match_details["configured_at"]) + '.dem',
                                demo_id=nickname + "_" + match_details["voting"]["map"]["pick"][0] + "_" + str(match_details["configured_at"]) + "_" + match_name,
                                parse_rate=128, 
                                outpath = 'demo_csgo/DataBase/' + match_details["voting"]["map"]["pick"][0] + '/')
        data = demo_parser.parse()
        print("parse success")

        os.remove('demo_csgo/DataBase/' + match_details["voting"]["map"]["pick"][0] + "_" + str(
            match_details["configured_at"]) + '.dem')
        os.remove('demo_csgo/DataBase/' + match_details["voting"]["map"]["pick"][0] + "_" + str(
            match_details["configured_at"]) + '.dem.7z')
    #    os.remove(str(match_details["configured_at"]) + ".json")
    #    match_name = all_match_player["items"][i]["match_id"]

     #   with open('demo_csgo/DataBase/' + match_details["voting"]["map"]["pick"][0] + '/' + nickname + "_" +
     #               match_details["voting"]["map"]["pick"][0] + "_" + str(
       #         match_details["configured_at"]) + "_" + match_name + '.json', 'w') as json_file:
       #     json.dump(data, json_file)
        print(match_details["voting"]["map"]["pick"][0]+"_"+str(match_details["configured_at"])+"_"+match_name)
        
    except:
        print("error, try next : ",r.status_code)
        os.remove('demo_csgo/DataBase/'+match_details["voting"]["map"]["pick"][0]+"_"+str(match_details["configured_at"])+'.dem.7z')
        os.system('clear')

