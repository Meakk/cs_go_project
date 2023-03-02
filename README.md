# cs_go_project

To Do : 
    - Create small front with flask to see match analysis on it -> DONE
    - Contenerize the app -> DONE 
    - Contenerize the match analysis (share volume between host and container for database)  -> DONE
    - Contenerize program that download with python API the matches and store it in database -> COMPLICATED AND NOT USEFULL
    - Use multiprocessing in python to optimize the download, the analysis
    - Replace JSON file analysis with python to pyspark to use parralization and multiprocessing
    

share container with host file : docker run -it --rm -v ${pwd}/demo_csgo:/demo_csgo busybox sh