<h1>cs_go_project</h1>

<h2>Context</h2>
<img src=https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQRhL-0BS-8I-UMKqUWSYJKuuMJ4_oB6uDL9Wyv6yQ&s>
<p>Counter-Strike: Global Offensive (CS:GO) is a popular multiplayer first-person shooter video game developed by Valve Corporation. In the game, players join either the Terrorist or Counter-Terrorist team and must complete objectives or eliminate the enemy team. It has a competitive mode where players can compete against each other in ranked matches.</p>

<p>FACEIT is a third-party online platform that provides competitive matchmaking and leagues for Counter-Strike: Global Offensive players. It offers players an opportunity to compete in high-level matches, tournaments, and leagues with rankings and rewards. Additionally, FACEIT also has an anti-cheat system to ensure fair play.</p>

<h2>Purpose of this project</h2>

<p>When Faceit finds you a match/lobby, you have 5 minutes to go on the server and play. The purpose of this project is to be able to automatically download the previous matches of your opponent and automatically analyze them to know recurrent strategy and their style of gameplay to know how to counter them in less than 5 minutes, before the game starts. Isn't it Counter-Strike?</p>

<h2>How it works</h2>

<ul>
  <li><strong>demo_csgo:</strong> This is the database of this application. This is where all the downloads, extraction, and parsing occur.</li>
  <li><strong>cs_go_analyse:</strong> This folder is where all the data analysis and data transformation occur.</li>
  <li><strong>download_matches:</strong> This folder contains all the application that will manage demo_csgo database.</li>
  <li><strong>Faceit API:</strong> Used to find and download matches.</li>
  <li><strong>awpy:</strong> Used to convert dem file downloaded to json file or csv dataframe. This will be our base for data analysis. Here an exemple of what the data look like : </li>
  
![data_show](https://user-images.githubusercontent.com/66355122/222761345-6e5db062-cc57-46ba-818a-39f9e4231e80.png)

</ul>

<h3>Done:</h3>

<ul>
  <li>Used API of FACEIT to automatically download matches of an opponent with nickname + map name as input.</li>
  <li>Managed the directory of the database.</li>
  <li>Transformed the data to create new information and use it to find new insights.</li>
  <li>Analyzed general style of gameplay and some insights. For exemple : Usual start positionement for pistol round (1 row = 1 match and the probability column tell us the % of times they used this start), rapidity of their gameplay during the Terrorist side (mean, meadian, std, number of data) and bombsite preference in % during the Terrorist side</li>
  
  ![positonnement](https://user-images.githubusercontent.com/66355122/222741706-a835322b-c28a-4c45-bcc3-fd097dc9cb77.png)
  
![data](https://user-images.githubusercontent.com/66355122/222755832-02debfc2-b3f6-4975-8670-04a13bbbe75a.png)


  <li>Visualized the opponent's strategy for both pistol rounds (Counter-terrorist and terrorist). One color = one match.</li>
  
![position](https://user-images.githubusercontent.com/66355122/222739768-39b5c244-b1d8-4c55-a81d-f6b4fe7accb9.png)

  ![télécharger](https://user-images.githubusercontent.com/66355122/222739762-a4853ba8-06bc-43a7-8770-799b943b7f6d.png)


  <li>Created a small front-end with a Flask application to visualize the data analysis.</li>

</ul>

<h3>To Do:</h3>

<ul>
  <li>Create a small front with Flask to see match analysis on it -> DONE</li>
  <li>Containerize the app -> Got problem to connect the app to internet in order to download the matches. See if I have to use a proxy. </li>
  <li>Containerize the match analysis (share volume between host and container for database) -> DONE</li>
  <li>Use multiprocessing in Python to optimize the download, the analysis.</li>
  <li>Replace JSON file analysis with Python to PySpark to use parallelization and multiprocessing.</li>
</ul>

<h3>Wish list of features:</h3>

<ul>
  <li>Machine learning model to automatically give the counter strategy.</li>
  <li>Deep learning model that is able to comment on the play of the opponent team and predict their next movement.</li>
  <li>Optimize data visualization with, for example, video graph showing their usual pistol, etc.</li>
</ul>

![plot](C:/Users/tlejoux/Downloads/position.png)
 
 <h2>Thanks</h2>
   <p>Thanks to the other github that I used for this project : https://github.com/pnxenopoulos/awpy from <strong>pnxenopoulos</strong> to parse the data and convert the dem file to json.<p>
   <p>Thanks to the faceit API<p>
share container with host file : docker run -it --rm -v ${pwd}/demo_csgo:/demo_csgo busybox sh
