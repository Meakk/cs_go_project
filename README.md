# cs_go_project

To Do : 
    - Create small front with flask to see match analysis on it
    - Contenerize the app 
    - Contenerize the match analysis (share volume between host and container for database) / maybe can contenerize the app with match analysis
    - Contenerize program that download with python API the matches and store it in database
    

share container with host file : docker run -it --rm -v ${pwd}/demo_csgo:/demo_csgo busybox sh