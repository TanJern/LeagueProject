from itertools import count
import queue
from riotwatcher import LolWatcher, ApiError
import numpy as np
import matplotlib.pyplot as plt
import pathlib
import pandas as pd
import seaborn as sns
import io, sys
sys.stdin = io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8')
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')


lol_watcher = LolWatcher('RGAPI-7d0f488f-180c-4263-a728-6d22329ba4e3')
my_region = 'na1'

#me = lol_watcher.summoner.by_name(my_region, 'Rectibility')
#print(me)
#my_ranked_stats = lol_watcher.league.by_summoner(my_region, me['id'])
#print(my_ranked_stats)


# First we get the latest version of the game from data dragon
versions = lol_watcher.data_dragon.versions_for_region(my_region)
champions_version = versions['n']['champion']


#GET CHALLENGER PLAYERS
player_region='NA1'.lower()
player_routing='americas'
queue_type='RANKED_SOLO_5x5'
num_matches_data=5
challenger_players=pd.DataFrame.from_dict(lol_watcher.league.challenger_by_queue(region=player_region,queue=queue_type)['entries'])
challenger_players=challenger_players.sort_values(by ='leaguePoints', ascending=False)
challenger_players.reset_index(drop=True, inplace=True)
summoner_names=challenger_players['summonerName'].tolist()
summoner_names=summoner_names[0:10]


all_matchlist=[] 
for summonerName in summoner_names:
    summoner=lol_watcher.summoner.by_name(player_region,summonerName)
    match_history=lol_watcher.match.matchlist_by_puuid(region=player_routing,puuid=summoner['puuid'],queue=420,start=0,count=num_matches_data)
    all_matchlist+=match_history
#print(all_matchlist)   
        


#Find champions in each match
champions_list=[]
for matchID in  all_matchlist:
    match_data=lol_watcher.match.by_id(region=player_routing,match_id=matchID)
    game_participants=match_data['info']['participants']
    for n in game_participants:
        champions_list.append(n['championName'])
#print(f"Champions from match history:",champions_list)
        


# All champions
current_champ_list = lol_watcher.data_dragon.champions(champions_version)["data"]
#print(current_champ_list['Ahri']['tags'])



#All mages
Mages=[x for x in current_champ_list if "Mage" in current_champ_list[x]['tags']]
#print(Mages)
#print(f"Total mages:",len(Mages))


#Filtering champion mages
played_mages=[]
for champions in champions_list:
    if champions in Mages:
        played_mages.append(champions)
    else:
        pass
#print(f"Mages in Games:",played_mages)


#Frequency of mages played
my_count = pd.Series(played_mages).value_counts()
print(my_count)
