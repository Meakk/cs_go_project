# cs_go_project

Context :

Counter-Strike: Global Offensive (CS:GO) is a popular multiplayer first-person shooter video game developed by Valve Corporation. In the game, players join either the Terrorist or Counter-Terrorist team and must complete objectives or eliminate the enemy team. It has a competitive mode where players can compete against each other in ranked matches.

FACEIT is a third-party online platform that provides competitive matchmaking and leagues for Counter-Strike: Global Offensive players. It offers players an opportunity to compete in high-level matches, tournaments and leagues with rankings and rewards. Additionally, FACEIT also has an anti-cheat system to ensure fair play.

Purpose of this project :

When Faceit finds you a match/ lobby, you have 5 min to go on the server and play. The purpose of this project is to be able in less than 5 minutes : automaticaly download the previous matches of your oppenent and automaticaly analyse them to know reccurent strategy and their style of gameplay in order to counter them. isn't it counter strike ?

How it works :
    - demo_csgo : This is the database of this application. This is where all the downloads, extraction, parsing  occurs,
    - cs_go_analyse : This folder is where all the data analysis and data transformation occurs,
    - download_matches : This folder contains all the application that will manage demo_csgo database.

Done :
    - API use of faceit to automaticaly download matches of an oppenent with nickname + map name as input,
    - Managing the directory DataBase,
    - Data transformation to create new information and use it to find new insight,
    - Data analysis of general style of gameplay and some insights,
    - Data visualisation of their strategy for both pistol rounds (Counter-terrorist and terrorist)
    - Small front-end with flask application to visualize the data analysis.


To Do : 
    - Create small front with flask to see match analysis on it -> DONE
    - Contenerize the app -> DONE 
    - Contenerize the match analysis (share volume between host and container for database)  -> DONE
    - Contenerize program that download with python API the matches and store it in database -> COMPLICATED AND NOT USEFULL
    - Use multiprocessing in python to optimize the download, the analysis
    - Replace JSON file analysis with python to pyspark to use parralization and multiprocessing

Wish list of features :
    - Machine learning model to automaticaly gives the counter strategy
    - Deep learning model that is able to comment the play of the oppenent team and predict their next movement
    - Optimize data visualisation with for exemple video graph showing their usual pistol etc
    
share container with host file : docker run -it --rm -v ${pwd}/demo_csgo:/demo_csgo busybox sh