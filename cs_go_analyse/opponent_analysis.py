# from Match_recuperation.Data_Parse import *
from .Graphic_build.coord_managing import *
from .Graphic_build.heatmap import *
from .Graphic_build.vectorization import coordonee_bomb_site
from .Graphic_build.vectorization import distance_point
import json
import re
import numpy as np
import os
import imageio
from IPython.display import display


def read_all_csgo_match_of_one_map_json(map_wanted):
    list_match = []
    print("map_wanted :", map_wanted)
    for root, dirs, files in os.walk("demo_csgo/DataBase/" + map_wanted):
        for filename in files:
            pattern = "(.*?).json"
            filename = re.search(pattern, filename).group(1)
            print(filename)
            with open(
                "demo_csgo/DataBase/" + map_wanted + "/" + filename + ".json"
            ) as file:
                data = json.load(file)
                list_match.append(data)
    return list_match


def pistol_analysis(player_name, map_select, list_match, side="t", start_frame=7):
    gif_frames = []
    for frame in range(start_frame, start_frame + 1, 1):
        dataframe_position_final = pd.DataFrame(columns=["x", "y"])
        dataframe_grenade = pd.DataFrame(columns=["x", "y", "info"])
        bombsite = []
        # list_match = read_all_csgo_match_of_one_map_json(map_select)
        kit = 0
        prob_place = pd.DataFrame()
        cpt = 0
        list_cpt = []
        for num_match in range(len(list_match)):
            round_t = 0
            for i in range(
                len(
                    list_match[num_match]["gameRounds"][round_t]["frames"][frame][side][
                        "players"
                    ]
                )
            ):
                if (
                    list_match[num_match]["gameRounds"][0]["frames"][frame][side][
                        "players"
                    ][i]["name"]
                    == player_name
                ):
                    round_t = 0
                    break
                else:
                    round_t = 15

            bombsiteA, bombsiteB = coordonee_bomb_site(list_match[0])
            bomb = [
                list_match[num_match]["gameRounds"][round_t]["frames"][-1]["bomb"]["x"],
                list_match[num_match]["gameRounds"][round_t]["frames"][-1]["bomb"]["y"],
                list_match[num_match]["gameRounds"][round_t]["frames"][-1]["bomb"]["z"],
            ]
            distA = distance_point(bomb, bombsiteA, map_select)
            distB = distance_point(bomb, bombsiteB, map_select)
            if distA <= distB:
                for i in range(5):
                    bombsite.append("A")
                    list_cpt.append(cpt)
                cpt += 1
            else:
                for i in range(5):
                    bombsite.append("B")
                    list_cpt.append(cpt)
                cpt += 1

            place = pd.DataFrame(index=["position_match" + str(num_match)])
            for player_id in range(
                len(list_match[num_match]["gameRounds"][round_t]["frames"][frame][side])
                - 1
            ):
                try:
                    place[
                        list_match[num_match]["gameRounds"][round_t]["frames"][frame][
                            side
                        ]["players"][player_id]["lastPlaceName"]
                    ] += 1
                    if (
                        (side == "ct")
                        & (
                            list_match[num_match]["gameRounds"][round_t]["frames"][
                                frame
                            ]["ct"]["players"][player_id]["hasDefuse"]
                        )
                        & (kit <= num_match)
                    ):
                        kit += 1
                except:
                    place[
                        list_match[num_match]["gameRounds"][round_t]["frames"][frame][
                            side
                        ]["players"][player_id]["lastPlaceName"]
                    ] = 1
                    if (
                        (side == "ct")
                        & (
                            list_match[num_match]["gameRounds"][round_t]["frames"][
                                frame
                            ]["ct"]["players"][player_id]["hasDefuse"]
                        )
                        & (kit <= num_match)
                    ):
                        kit += 1
            round_num = list_match[num_match]["gameRounds"][round_t]["roundNum"]
            clock = list_match[num_match]["gameRounds"][round_t]["frames"][frame][
                "clockTime"
            ]
            dataframe_position_final = get_coord_dataframe_with_info(
                map_select,
                list_match[num_match]["gameRounds"][round_t]["frames"][frame][side][
                    "players"
                ],
                "x",
                "y",
                "z",
                dataframe_position_final,
                clock,
                round_num,
                ["name", "activeWeapon"],
            )
            # dataframe_grenade = get_coord_dataframe_with_info(map_select, list_match[num_match]["gameRounds"][round_t]['grenades'], "grenadeX", "grenadeY",dataframe_grenade, ["grenadeType",'throwClockTime',"throwerSide"])
            prob_place = pd.concat([place, prob_place]).fillna(0)

        if side == "ct":
            print("Kit prob :", kit)

        prob_place = (
            prob_place.groupby(prob_place.columns.tolist())
            .size()
            .reset_index()
            .rename(columns={0: "records"})
        )
        prob_place["prob"] = prob_place["records"] / len(list_match)
        prob_place = prob_place.drop("records", axis=1)
        if side == "t":
            SIDE = "T"
        else:
            SIDE = "CT"
        dataframe_grenade = dataframe_grenade[
            pd.Series([("," + SIDE in e) for e in dataframe_grenade["info"]])
        ].reset_index(drop=True)
        dataframe_position_final["Bombsite"] = bombsite
        dataframe_position_final["Match_ID"] = list_cpt
        dataframe_grenade["Bombsite"] = len(dataframe_grenade) * [None]
        dataframe_grenade["Match_ID"] = len(dataframe_grenade) * [None]

        data_player = plot_map_list_of_game(
            dataframe_position_final,
            map_select,
            frame=frame,
            text=True,
            nb_games=len(list_match),
            color_set="Match_ID",
        )
        image = imageio.v2.imread(f"./demo_csgo/img/img_{frame}.png")
        gif_frames.append(image)
    imageio.mimsave(
        f"demo_csgo/img/{side}.gif",  # output gif
        gif_frames,  # array of input frames
        duration=1000,
    )  # optional: frames per second

    # if not dataframe_grenade.empty:
    #   data_grenade = plot_map_list_of_game(dataframe_grenade, map_select, text = True,nb_games = len(list_match))

    return prob_place, data_player


def grenade_analysis(dic_list, map_select, x, y, text=False, info=None):
    dataframe_position_final = get_coord_dataframe(
        map_select, dic_list, x, y, text, info
    )
    plot_map_list_of_game(dataframe_position_final, map_select, text)
    return dataframe_position_final


def fav_bomb_site_analysis(player_name, list_match, map_select, side="t", frame=-1):
    # list_match = read_all_csgo_match_of_one_map_json(map_select)

    bombsiteA, bombsiteB = coordonee_bomb_site(list_match[0])

    round_time_before_plant_Full_Eco = []
    round_time_before_plant_Semi_Eco = []
    round_time_before_plant_Semi_Buy = []
    round_time_before_plant_Full_Buy = []
    round_time_before_plant_pistol = []
    round_time_before_plant_ct_eco = []

    Full_Eco_a = 0
    Semi_Eco_a = 0
    Semi_Buy_a = 0
    Full_Buy_a = 0
    Full_Eco_b = 0
    Semi_Eco_b = 0
    Semi_Buy_b = 0
    Full_Buy_b = 0

    ct_Full_Eco_a = 0
    ct_Full_Eco_b = 0

    pistol_t_b = 0
    pistol_t_a = 0
    bomb_dataframe = pd.DataFrame(columns=["x", "y", "z", "side_A"])

    for num_match in range(len(list_match)):
        round_t = 0
        for i in range(
            len(
                list_match[num_match]["gameRounds"][round_t]["frames"][frame][side][
                    "players"
                ]
            )
        ):
            if (
                list_match[num_match]["gameRounds"][0]["frames"][frame][side][
                    "players"
                ][i]["name"]
                == player_name
            ):
                round_t = 0
                break
            else:
                round_t = 15
        for round in range(
            round_t,
            int(round_t * len(list_match[num_match]["gameRounds"]) / 15 + 15 - round_t),
        ):
            buy_type = list_match[num_match]["gameRounds"][round]["tBuyType"]
            ct_buy_type = list_match[num_match]["gameRounds"][round]["ctBuyType"]
            bomb = [
                list_match[num_match]["gameRounds"][round]["frames"][frame]["bomb"][
                    "x"
                ],
                list_match[num_match]["gameRounds"][round]["frames"][frame]["bomb"][
                    "y"
                ],
                list_match[num_match]["gameRounds"][round]["frames"][frame]["bomb"][
                    "z"
                ],
            ]
            distA = distance_point(bomb, bombsiteA, map_select)
            distB = distance_point(bomb, bombsiteB, map_select)
            bomb_list = {
                "x": pointx_to_resolutionx(bomb[0], map_select),
                "y": pointy_to_resolutiony(bomb[1], map_select),
                "z": bomb[2],
                "side_A": distA < distB,
            }
            bomb_dataframe = pd.concat(
                [bomb_dataframe, pd.DataFrame([bomb_list])], ignore_index=True
            )
            if distA <= distB:
                if (round != 15) | (round != 0):
                    if buy_type == "Full Eco":
                        Full_Eco_a += 1
                    if buy_type == "Semi Eco":
                        Semi_Eco_a += 1
                    if buy_type == "Semi Buy":
                        Semi_Buy_a += 1
                    if buy_type == "Full Buy":
                        Full_Buy_a += 1

                    if ct_buy_type == "Semi Eco":
                        ct_Full_Eco_a += 1
                    if ct_buy_type == "Full Eco":
                        ct_Full_Eco_a += 1

                if (round == 15) | (round == 0):
                    pistol_t_a += 1

            if distB < distA:
                if (round != 15) | (round != 0):
                    if buy_type == "Full Eco":
                        Full_Eco_b += 1
                    if buy_type == "Semi Eco":
                        Semi_Eco_b += 1
                    if buy_type == "Semi Buy":
                        Semi_Buy_b += 1
                    if buy_type == "Full Buy":
                        Full_Buy_b += 1

                    if ct_buy_type == "Semi Eco":
                        ct_Full_Eco_b += 1
                    if ct_buy_type == "Full Eco":
                        ct_Full_Eco_b += 1

                if (round == 15) | (round == 0):
                    pistol_t_b += 1

            # mean time round
            if (round == 15) | (round == 0):
                round_duration = list_match[num_match]["gameRounds"][round]["frames"][
                    -1
                ]["seconds"]
                for i in list_match[num_match]["gameRounds"][round]["bombEvents"]:
                    if i["bombAction"] == "plant":
                        round_duration = i["seconds"]
                        break
                round_time_before_plant_pistol.append(round_duration)

            if (buy_type == "Full Eco") & ((round != 15) | (round != 0)):
                round_duration = list_match[num_match]["gameRounds"][round]["frames"][
                    -1
                ]["seconds"]
                for i in list_match[num_match]["gameRounds"][round]["bombEvents"]:
                    if i["bombAction"] == "plant":
                        round_duration = i["seconds"]
                        break
                round_time_before_plant_Full_Eco.append(round_duration)

            if (buy_type == "Semi Eco") & ((round != 15) | (round != 0)):
                round_duration = list_match[num_match]["gameRounds"][round]["frames"][
                    -1
                ]["seconds"]
                for i in list_match[num_match]["gameRounds"][round]["bombEvents"]:
                    if i["bombAction"] == "plant":
                        round_duration = i["seconds"]
                        break
                round_time_before_plant_Semi_Eco.append(round_duration)

            if (buy_type == "Semi Buy") & ((round != 15) | (round != 0)):
                round_duration = list_match[num_match]["gameRounds"][round]["frames"][
                    -1
                ]["seconds"]
                for i in list_match[num_match]["gameRounds"][round]["bombEvents"]:
                    if i["bombAction"] == "plant":
                        round_duration = i["seconds"]
                        break
                round_time_before_plant_Semi_Buy.append(round_duration)

            if (buy_type == "Full Buy") & ((round != 15) | (round != 0)):
                round_duration = list_match[num_match]["gameRounds"][round]["frames"][
                    -1
                ]["seconds"]
                for i in list_match[num_match]["gameRounds"][round]["bombEvents"]:
                    if i["bombAction"] == "plant":
                        round_duration = i["seconds"]
                        break
                round_time_before_plant_Full_Buy.append(round_duration)

            if ((ct_buy_type == "Full Eco") | (ct_buy_type == "Semi Eco")) & (
                (round != 15) | (round != 0)
            ):
                round_duration = list_match[num_match]["gameRounds"][round]["frames"][
                    -1
                ]["seconds"]
                for i in list_match[num_match]["gameRounds"][round]["bombEvents"]:
                    if i["bombAction"] == "plant":
                        round_duration = i["seconds"]
                        break
                round_time_before_plant_ct_eco.append(round_duration)

    round_time_before_plant_Full_Eco = np.array(round_time_before_plant_Full_Eco)
    round_time_before_plant_Semi_Eco = np.array(round_time_before_plant_Semi_Eco)
    round_time_before_plant_Semi_Buy = np.array(round_time_before_plant_Semi_Buy)
    round_time_before_plant_Full_Buy = np.array(round_time_before_plant_Full_Buy)
    round_time_before_plant_pistol = np.array(round_time_before_plant_pistol)
    round_time_before_plant_ct_eco = np.array(round_time_before_plant_ct_eco)

    data = pd.DataFrame(
        index=[
            "Full_eco_T",
            "Semi_eco_T",
            "Semi_buy_T",
            "Full_buy_T",
            "CT_in_Eco",
            "Pistol_rounds",
        ],
        columns=[
            "prob_go_A",
            "prob_go_B",
            "Mean_Sec_Round_before_plant(s)",
            "Med_Sec_Round_before_plant(s)",
            "std_Sec_Round_before_plant",
            "nb_sample",
        ],
        data=(
            [
                [
                    Full_Eco_a / (Full_Eco_a + Full_Eco_b),
                    Full_Eco_b / (Full_Eco_a + Full_Eco_b),
                    round_time_before_plant_Full_Eco.mean(),
                    np.median(round_time_before_plant_Full_Eco),
                    round_time_before_plant_Full_Eco.std(),
                    len(round_time_before_plant_Full_Eco),
                ],
                [
                    Semi_Eco_a / (Semi_Eco_a + Semi_Eco_b),
                    Semi_Eco_b / (Semi_Eco_a + Semi_Eco_b),
                    round_time_before_plant_Semi_Eco.mean(),
                    np.median(round_time_before_plant_Semi_Eco),
                    round_time_before_plant_Semi_Eco.std(),
                    len(round_time_before_plant_Semi_Eco),
                ],
                [
                    Semi_Buy_a / (Semi_Buy_a + Semi_Buy_b),
                    Semi_Buy_b / (Semi_Buy_a + Semi_Buy_b),
                    round_time_before_plant_Semi_Buy.mean(),
                    np.median(round_time_before_plant_Semi_Buy),
                    round_time_before_plant_Semi_Buy.std(),
                    len(round_time_before_plant_Semi_Buy),
                ],
                [
                    Full_Buy_a / (Full_Buy_a + Full_Buy_b),
                    Full_Buy_b / (Full_Buy_a + Full_Buy_b),
                    round_time_before_plant_Full_Buy.mean(),
                    np.median(round_time_before_plant_Full_Buy),
                    round_time_before_plant_Full_Buy.std(),
                    len(round_time_before_plant_Full_Buy),
                ],
                [
                    ct_Full_Eco_a / (ct_Full_Eco_a + ct_Full_Eco_b),
                    ct_Full_Eco_b / (ct_Full_Eco_a + ct_Full_Eco_b),
                    round_time_before_plant_ct_eco.mean(),
                    np.median(round_time_before_plant_ct_eco),
                    round_time_before_plant_ct_eco.std(),
                    len(round_time_before_plant_ct_eco),
                ],
                [
                    pistol_t_a / (pistol_t_a + pistol_t_b),
                    pistol_t_b / (pistol_t_a + pistol_t_b),
                    round_time_before_plant_pistol.mean(),
                    np.median(round_time_before_plant_pistol),
                    round_time_before_plant_pistol.std(),
                    len(round_time_before_plant_pistol),
                ],
            ]
        ),
    )

    # data_bomb = plot_map_list_of_game(dataframe_position_final, map_select,frame = frame,text = True, nb_games = len(list_match),premade = premade)
    plot_from_df(bomb_dataframe, map_select)
    return data, bomb_dataframe


def round_analysis(
    player_name,
    map_select,
    list_match,
    side="t",
    frame=7,
    buy_type="Full Buy",
    premade=[],
):
    dataframe_position_final = pd.DataFrame(columns=["x", "y", "z"])
    dataframe_grenade = pd.DataFrame(columns=["x", "y", "info"])
    bombsite = []
    # list_match = read_all_csgo_match_of_one_map_json(map_select)
    kit = 0
    prob_place = pd.DataFrame()
    cpt = 0
    list_cpt = []
    cpt2 = -1
    match_id = []
    round_id = []
    for num_match in range(len(list_match)):
        round = 0
        if (num_match == 2) & (buy_type == "Full Buy"):
            break
        for i in range(
            len(
                list_match[num_match]["gameRounds"][round]["frames"][frame][side][
                    "players"
                ]
            )
        ):
            if (
                list_match[num_match]["gameRounds"][0]["frames"][frame][side][
                    "players"
                ][i]["name"]
                == player_name
            ):
                round = 0
                break
            else:
                round = 15
        for round_t in range(
            round,
            int(round * len(list_match[num_match]["gameRounds"]) / 15 + 15 - round),
        ):
            if (
                (
                    (side == "t")
                    & (
                        list_match[num_match]["gameRounds"][round_t]["tBuyType"]
                        != buy_type
                    )
                )
                | (round_t == 0)
                | (round_t == 15)
            ):
                # print(side,list_match[num_match]["gameRounds"][round_t]['tBuyType'],round_t)
                continue
            if (
                (
                    (side == "ct")
                    & (
                        list_match[num_match]["gameRounds"][round_t]["ctBuyType"]
                        != buy_type
                    )
                )
                | (round_t == 0)
                | (round_t == 15)
            ):
                # print(side,list_match[num_match]["gameRounds"][round_t]['ctBuyType'],round_t)
                continue
            cpt2 += 1
            bombsiteA, bombsiteB = coordonee_bomb_site(list_match[0])
            bomb = [
                list_match[num_match]["gameRounds"][round_t]["frames"][-1]["bomb"]["x"],
                list_match[num_match]["gameRounds"][round_t]["frames"][-1]["bomb"]["y"],
                list_match[num_match]["gameRounds"][round_t]["frames"][-1]["bomb"]["z"],
            ]
            distA = distance_point(bomb, bombsiteA, map_select)
            distB = distance_point(bomb, bombsiteB, map_select)
            if distA <= distB:
                for i in range(5):
                    bombsite.append("A")
                    match_id.append(num_match)
                    round_id.append(cpt2)
                cpt += 1
            else:
                for i in range(5):
                    bombsite.append("B")
                    match_id.append(num_match)
                    round_id.append(cpt2)
                cpt += 1

            place = pd.DataFrame(index=["position_match" + str(num_match)])
            for player_id in range(
                len(list_match[num_match]["gameRounds"][round_t]["frames"][frame][side])
                - 1
            ):
                try:
                    place[
                        list_match[num_match]["gameRounds"][round_t]["frames"][frame][
                            side
                        ]["players"][player_id]["lastPlaceName"]
                    ] += 1
                    if (
                        (side == "ct")
                        & (
                            list_match[num_match]["gameRounds"][round_t]["frames"][
                                frame
                            ]["ct"]["players"][player_id]["hasDefuse"]
                        )
                        & (kit <= num_match)
                    ):
                        kit += 1
                except:
                    place[
                        list_match[num_match]["gameRounds"][round_t]["frames"][frame][
                            side
                        ]["players"][player_id]["lastPlaceName"]
                    ] = 1
                    if (
                        (side == "ct")
                        & (
                            list_match[num_match]["gameRounds"][round_t]["frames"][
                                frame
                            ]["ct"]["players"][player_id]["hasDefuse"]
                        )
                        & (kit <= num_match)
                    ):
                        kit += 1
            round_num = list_match[num_match]["gameRounds"][round_t]["roundNum"] - round
            clock = list_match[num_match]["gameRounds"][round_t]["frames"][frame][
                "clockTime"
            ]
            dataframe_position_final = get_coord_dataframe_with_info(
                map_select,
                list_match[num_match]["gameRounds"][round_t]["frames"][frame][side][
                    "players"
                ],
                "x",
                "y",
                "z",
                dataframe_position_final,
                clock,
                round_num,
                ["name", "activeWeapon"],
            )
            # dataframe_grenade = get_coord_dataframe_with_info(map_select, list_match[num_match]["gameRounds"][round_t]['grenades'], "grenadeX", "grenadeY",dataframe_grenade, ["grenadeType",'throwClockTime',"throwerSide"])
            prob_place = pd.concat([place, prob_place]).fillna(0)
    if side == "ct":
        print("Kit prob :", kit)

    prob_place = (
        prob_place.groupby(prob_place.columns.tolist())
        .size()
        .reset_index()
        .rename(columns={0: "records"})
    )
    prob_place["prob"] = prob_place["records"] / len(list_match)
    prob_place = prob_place.drop("records", axis=1)
    if side == "t":
        SIDE = "T"
    else:
        SIDE = "CT"
    dataframe_grenade = dataframe_grenade[
        pd.Series([("," + SIDE in e) for e in dataframe_grenade["info"]])
    ].reset_index(drop=True)
    dataframe_position_final["Bombsite"] = bombsite
    dataframe_position_final["Match_ID"] = match_id
    dataframe_position_final["Round_id"] = round_id
    dataframe_grenade["Bombsite"] = len(dataframe_grenade) * [None]
    dataframe_grenade["Match_ID"] = len(dataframe_grenade) * [None]
    data_player = plot_map_list_of_game(
        dataframe_position_final,
        map_select,
        frame=frame,
        text=True,
        nb_games=len(list_match),
        premade=premade,
    )

    # if not dataframe_grenade.empty:
    #   data_grenade = plot_map_list_of_game(dataframe_grenade, map_select, text = True,nb_games = len(list_match))

    return prob_place, data_player


def ct_positionement_start(
    player_name, map_select, list_match, frame=7, buy_type="Full Buy"
):
    side = "ct"
    prob_place = pd.DataFrame()
    dataframe_position_final = pd.DataFrame(columns=["x", "y", "z"])
    cpt2 = 0
    bombsiteA, bombsiteB = coordonee_bomb_site(list_match[0])
    bombsiteA = [
        pointx_to_resolutionx(bombsiteA[0], map_select),
        pointy_to_resolutiony(bombsiteA[1], map_select),
        bombsiteA[2],
    ]
    bombsiteB = [
        pointx_to_resolutionx(bombsiteB[0], map_select),
        pointy_to_resolutiony(bombsiteB[1], map_select),
        bombsiteB[2],
    ]
    round_number = []
    round_compteur = 0

    frame_number = []
    for num_match in range(len(list_match)):
        round = 0
        cpt2 += 1
        if (cpt2 == 5) & (buy_type == "Full Buy"):
            break

        for i in range(
            len(
                list_match[num_match]["gameRounds"][round]["frames"][frame][side][
                    "players"
                ]
            )
        ):
            if (
                list_match[num_match]["gameRounds"][0]["frames"][frame][side][
                    "players"
                ][i]["name"]
                == player_name
            ):
                round = 0
                break
            else:
                round = 15

        for round_t in range(
            round,
            int(round * len(list_match[num_match]["gameRounds"]) / 15 + 15 - round),
        ):
            if (
                (side == "ct")
                & (buy_type != "Pistol Round")
                & (
                    list_match[num_match]["gameRounds"][round_t]["ctBuyType"]
                    != buy_type
                )
            ):
                continue
            if (round_t != 0) & (round_t != 15) & (buy_type == "Pistol Round"):
                continue
            place = pd.DataFrame(index=["position_match" + str(num_match)])
            round_compteur += 1
            for test_frame in range(4):
                test_frame = test_frame + frame

                for player_id in range(
                    len(
                        list_match[num_match]["gameRounds"][round_t]["frames"][
                            test_frame
                        ][side]
                    )
                    - 1
                ):
                    try:
                        place[
                            list_match[num_match]["gameRounds"][round_t]["frames"][
                                test_frame
                            ][side]["players"][player_id]["lastPlaceName"]
                        ] += 1
                        round_number.append(round_compteur)
                        frame_number.append(test_frame)
                    except:
                        place[
                            list_match[num_match]["gameRounds"][round_t]["frames"][
                                test_frame
                            ][side]["players"][player_id]["lastPlaceName"]
                        ] = 1
                        round_number.append(round_compteur)
                        frame_number.append(test_frame)

                round_num = (
                    list_match[num_match]["gameRounds"][round_t]["roundNum"] - round
                )
                clock = list_match[num_match]["gameRounds"][round_t]["frames"][
                    test_frame
                ]["clockTime"]
                dataframe_position_final = get_coord_dataframe_with_info(
                    map_select,
                    list_match[num_match]["gameRounds"][round_t]["frames"][test_frame][
                        side
                    ]["players"],
                    "x",
                    "y",
                    "z",
                    dataframe_position_final,
                    clock,
                    round_num,
                    ["name", "activeWeapon"],
                )
                # dataframe_grenade = get_coord_dataframe_with_info(map_select, list_match[num_match]["gameRounds"][round_t]['grenades'], "grenadeX", "grenadeY",dataframe_grenade, ["grenadeType",'throwClockTime',"throwerSide"])
                prob_place = pd.concat([place, prob_place]).fillna(0)
    cols = ["x", "y", "z"]

    dataframe_position_final["frame_number"] = frame_number
    dataframe_position_final["round_compteur"] = round_number
    dataframe_position_final["coord"] = dataframe_position_final[cols].values.tolist()
    dataframe_position_final["dist_a"] = dataframe_position_final["coord"].apply(
        lambda x: distance_point(x, bombsiteA, map_select)
    )
    dataframe_position_final["dist_b"] = dataframe_position_final["coord"].apply(
        lambda x: distance_point(x, bombsiteB, map_select)
    )
    dataframe_position_final["A_site"] = (
        dataframe_position_final["dist_a"] < dataframe_position_final["dist_b"]
    )
    df = dataframe_position_final.copy()
    dataframe_position_final = dataframe_position_final[
        dataframe_position_final["frame_number"] == 10
    ]
    # df = dataframe_position_final.copy()
    dataframe_position_final = dataframe_position_final.groupby("round_compteur").sum()
    dataframe_position_final["B_site"] = 5 - dataframe_position_final["A_site"]
    df3 = dataframe_position_final.groupby(["A_site", "B_site"]).count()
    df3["Proba"] = (
        dataframe_position_final.groupby(["A_site", "B_site"]).count()
        / len(dataframe_position_final)
        * 100
    )["x"]
    df3["nb_sample"] = (dataframe_position_final.groupby(["A_site", "B_site"]).count())[
        "x"
    ]
    df3 = df3[["Proba", "nb_sample"]]
    display(df3)
    if map_select == "de_inferno":
        # for frame in range(7,11,1):
        df["push_apps_inferno"] = (df["x"] < 690) & (df["y"] >= 760)
        df["push_B_inferno"] = (df["x"] < 530) & (df["y"] > 400) & (df["y"] < 560)
        df["push_mid_inferno"] = (df["x"] < 650) & (df["y"] < 750) & (df["y"] > 600)
        df = df.groupby(["round_compteur", "frame_number"]).sum()
        df4 = df.groupby(
            ["frame_number", "push_apps_inferno", "push_B_inferno", "push_mid_inferno"]
        ).count()
        print(df3["nb_sample"].sum())
        df4["Proba"] = (
            df.groupby(
                [
                    "frame_number",
                    "push_apps_inferno",
                    "push_B_inferno",
                    "push_mid_inferno",
                ]
            ).count()
            / df3["nb_sample"].sum()
            * 100
        )["x"]
        df4["nb_sample"] = (
            df.groupby(
                [
                    "frame_number",
                    "push_apps_inferno",
                    "push_B_inferno",
                    "push_mid_inferno",
                ]
            ).count()
        )["x"]
        df4 = df4[["Proba", "nb_sample"]]
        display(df4)
        df4 = df4.groupby(
            ["push_apps_inferno", "push_B_inferno", "push_mid_inferno"]
        ).max()
        display(df4)

    return df3


def second_round(
    player_name,
    map_select,
    list_match,
    side="t",
    frame=7,
    buy_type="Full Buy",
    premade=[],
    winning_gr_side="T",
):
    dataframe_position_final = pd.DataFrame(columns=["x", "y", "z"])
    dataframe_grenade = pd.DataFrame(columns=["x", "y", "info"])
    bombsite = []
    # list_match = read_all_csgo_match_of_one_map_json(map_select)
    kit = 0
    prob_place = pd.DataFrame()
    cpt = 0
    list_cpt = []
    cpt2 = -1
    match_id = []
    round_id = []
    for num_match in range(len(list_match)):
        round = 0
        for i in range(
            len(
                list_match[num_match]["gameRounds"][round]["frames"][frame][side][
                    "players"
                ]
            )
        ):
            if (
                list_match[num_match]["gameRounds"][0]["frames"][frame][side][
                    "players"
                ][i]["name"]
                == player_name
            ):
                round_t = 1
                break
            else:
                round_t = 16
        if (
            list_match[num_match]["gameRounds"][round_t - 1]["winningSide"]
            != winning_gr_side
        ):
            print(
                list_match[num_match]["gameRounds"][round_t - 1]["winningSide"],
                winning_gr_side,
            )
            # print(side,list_match[num_match]["gameRounds"][round_t]['tBuyType'],round_t)
            continue
        cpt2 += 1
        bombsiteA, bombsiteB = coordonee_bomb_site(list_match[0])
        bomb = [
            list_match[num_match]["gameRounds"][round_t]["frames"][-1]["bomb"]["x"],
            list_match[num_match]["gameRounds"][round_t]["frames"][-1]["bomb"]["y"],
            list_match[num_match]["gameRounds"][round_t]["frames"][-1]["bomb"]["z"],
        ]
        distA = distance_point(bomb, bombsiteA, map_select)
        distB = distance_point(bomb, bombsiteB, map_select)
        if distA <= distB:
            for i in range(5):
                bombsite.append("A")
                match_id.append(num_match)
                round_id.append(cpt2)
            cpt += 1
        else:
            for i in range(5):
                bombsite.append("B")
                match_id.append(num_match)
                round_id.append(cpt2)
            cpt += 1

        place = pd.DataFrame(index=["position_match" + str(num_match)])
        for player_id in range(
            len(list_match[num_match]["gameRounds"][round_t]["frames"][frame][side]) - 1
        ):
            try:
                place[
                    list_match[num_match]["gameRounds"][round_t]["frames"][frame][side][
                        "players"
                    ][player_id]["lastPlaceName"]
                ] += 1
                if (
                    (side == "ct")
                    & (
                        list_match[num_match]["gameRounds"][round_t]["frames"][frame][
                            "ct"
                        ]["players"][player_id]["hasDefuse"]
                    )
                    & (kit <= num_match)
                ):
                    kit += 1
            except:
                place[
                    list_match[num_match]["gameRounds"][round_t]["frames"][frame][side][
                        "players"
                    ][player_id]["lastPlaceName"]
                ] = 1
                if (
                    (side == "ct")
                    & (
                        list_match[num_match]["gameRounds"][round_t]["frames"][frame][
                            "ct"
                        ]["players"][player_id]["hasDefuse"]
                    )
                    & (kit <= num_match)
                ):
                    kit += 1
        round_num = list_match[num_match]["gameRounds"][round_t]["roundNum"] - round
        clock = list_match[num_match]["gameRounds"][round_t]["frames"][frame][
            "clockTime"
        ]
        dataframe_position_final = get_coord_dataframe_with_info(
            map_select,
            list_match[num_match]["gameRounds"][round_t]["frames"][frame][side][
                "players"
            ],
            "x",
            "y",
            "z",
            dataframe_position_final,
            clock,
            round_num,
            ["name", "activeWeapon"],
        )
        # dataframe_grenade = get_coord_dataframe_with_info(map_select, list_match[num_match]["gameRounds"][round_t]['grenades'], "grenadeX", "grenadeY",dataframe_grenade, ["grenadeType",'throwClockTime',"throwerSide"])
        prob_place = pd.concat([place, prob_place]).fillna(0)
    if side == "ct":
        print("Kit prob :", kit)

    prob_place = (
        prob_place.groupby(prob_place.columns.tolist())
        .size()
        .reset_index()
        .rename(columns={0: "records"})
    )
    prob_place["prob"] = prob_place["records"] / len(list_match)
    prob_place = prob_place.drop("records", axis=1)
    if side == "t":
        SIDE = "T"
    else:
        SIDE = "CT"
    dataframe_grenade = dataframe_grenade[
        pd.Series([("," + SIDE in e) for e in dataframe_grenade["info"]])
    ].reset_index(drop=True)
    dataframe_position_final["Bombsite"] = bombsite
    dataframe_position_final["Match_ID"] = match_id
    dataframe_position_final["Round_id"] = round_id
    dataframe_grenade["Bombsite"] = len(dataframe_grenade) * [None]
    dataframe_grenade["Match_ID"] = len(dataframe_grenade) * [None]
    data_player = plot_map_list_of_game(
        dataframe_position_final,
        map_select,
        frame=frame,
        text=True,
        nb_games=len(list_match),
        premade=premade,
    )


def ct_kill_position(player_name, map_select, list_match, premade):
    for joueur in premade:
        dataframe_position_final = pd.DataFrame(
            columns=["player", "clock", "x", "y", "z", "weapon"]
        )
        side = "ct"
        frame = 7
        for num_match in range(len(list_match)):
            round = 0

            for i in range(
                len(
                    list_match[num_match]["gameRounds"][round]["frames"][frame][side][
                        "players"
                    ]
                )
            ):
                if (
                    list_match[num_match]["gameRounds"][0]["frames"][frame][side][
                        "players"
                    ][i]["name"]
                    == player_name
                ):
                    round = 0
                    break
                else:
                    round = 15

            for round_t in range(
                round,
                int(round * len(list_match[num_match]["gameRounds"]) / 15 + 15 - round),
            ):
                for killer in list_match[num_match]["gameRounds"][round_t]["kills"]:
                    if (killer["attackerSide"] == "CT") & (
                        killer["attackerName"] in (joueur)
                    ):
                        player_dict = {
                            "player": killer["attackerName"],
                            "x": killer["attackerX"],
                            "y": killer["attackerY"],
                            "z": killer["attackerZ"],
                            "clock": killer["clockTime"],
                            "weapon": killer["weapon"],
                        }
                        dataframe_position_final = pd.concat(
                            [
                                pd.DataFrame.from_dict(player_dict, orient="index").T,
                                dataframe_position_final,
                            ],
                            axis=0,
                        ).reset_index(drop=True)

        dataframe_position_final["x"] = dataframe_position_final["x"].apply(
            lambda x: pointx_to_resolutionx(x, map_select)
        )
        dataframe_position_final["y"] = dataframe_position_final["y"].apply(
            lambda x: pointy_to_resolutiony(x, map_select)
        )

        plot_from_simple_df(dataframe_position_final, map_select)
