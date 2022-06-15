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


lol_watcher = LolWatcher('ENTER API KEY')

# First we get the latest version of the game from data dragon
my_region = 'na1'
my_region2 = 'euw1'
versions = lol_watcher.data_dragon.versions_for_region(my_region)
versions2 = lol_watcher.data_dragon.versions_for_region(my_region2)
champions_version = versions['n']['champion']
champions_version2 = versions['n']['champion']


# All champions
current_champ_list = lol_watcher.data_dragon.champions(champions_version)["data"]
current_champ_list2 = lol_watcher.data_dragon.champions(champions_version2)["data"]
#print(current_champ_list['Ahri']['tags']) Finding info on specific champion


#NA PLAYERS INFO
player_region='NA1'.lower()
player_routing='americas'
queue_type='RANKED_SOLO_5x5'
num_matches_data=5

#EUW PLAYERS INFO
player_region2='EUW1'.lower()
player_routing2='europe'


#GET SUMMONER NAMES OF NA PLAYERS
def get_summoners():
    challenger_players=pd.DataFrame.from_dict(lol_watcher.league.challenger_by_queue(region=player_region,queue=queue_type)['entries'])
    challenger_players=challenger_players.sort_values(by ='leaguePoints', ascending=False)
    challenger_players.reset_index(drop=True, inplace=True)
    summoner_names=challenger_players['summonerName'].tolist()
    summoner_names=summoner_names[0:12]
    return summoner_names


#GET SUMMONER NAMES OF EUW PLAYERS
def get_summoners2():
    challenger_players=pd.DataFrame.from_dict(lol_watcher.league.challenger_by_queue(region=player_region2,queue=queue_type)['entries'])
    challenger_players=challenger_players.sort_values(by ='leaguePoints', ascending=False)
    challenger_players.reset_index(drop=True, inplace=True)
    summoner_names=challenger_players['summonerName'].tolist()
    summoner_names=summoner_names[0:12] 
    return summoner_names




#GET SUMMONERS' MATCH HISTORY
def get_matchlist(summoner_names):
    all_matchlist=[] 
    for summonerName in summoner_names:
        summoner=lol_watcher.summoner.by_name(player_region,summonerName)
        match_history=lol_watcher.match.matchlist_by_puuid(region=player_routing,puuid=summoner['puuid'],queue=420,start=0,count=num_matches_data)
        all_matchlist+=match_history 
    return all_matchlist 


def get_matchlist2(summoner_names):
    all_matchlist=[] 
    for summonerName in summoner_names:
        summoner=lol_watcher.summoner.by_name(player_region2,summonerName)
        match_history=lol_watcher.match.matchlist_by_puuid(region=player_routing2,puuid=summoner['puuid'],queue=420,start=0,count=num_matches_data)
        all_matchlist+=match_history 
    return all_matchlist 
        


#Find champions in each match
def ingame_champions(all_matchlist):
    champions_list=[]
    for matchID in  all_matchlist:
        match_data=lol_watcher.match.by_id(region=player_routing,match_id=matchID)
        game_participants=match_data['info']['participants']
        for n in game_participants:
            champions_list.append(n['championName'])
    #print(f"Champions from match history:",champions_list)
    return champions_list

def ingame_champions2(all_matchlist):
    champions_list=[]
    for matchID in  all_matchlist:
        match_data=lol_watcher.match.by_id(region=player_routing2,match_id=matchID)
        game_participants=match_data['info']['participants']
        for n in game_participants:
            champions_list.append(n['championName'])
    #print(f"Champions from match history:",champions_list)
    return champions_list
            


#All mages
def get_mages():
    Mages=[x for x in current_champ_list if "Mage" in current_champ_list[x]['tags']]
    #print(Mages)
    #print(f"Total mages:",len(Mages))
    return Mages

def get_mages2():
    Mages=[x for x in current_champ_list2 if "Mage" in current_champ_list2[x]['tags']]
    #print(Mages)
    #print(f"Total mages:",len(Mages))
    return Mages



#Filtering Mages Champions
def ingame_mages(champions_list,Mages):
    played_mages=[]
    for champions in champions_list:
        if champions in Mages:
            played_mages.append(champions)
        else:
            pass
    #print(f"Mages in NA Games:",played_mages)
    return played_mages

def ingame_mages2(champions_list,Mages):
    played_mages=[]
    for champions in champions_list:
        if champions in Mages:
            played_mages.append(champions)
        else:
            pass
    #print(f"Mages in EU Games:",played_mages)
    return played_mages



#Frequency of Mage Champions played
def count_item(item,lst):
    return len([x for x in lst if x==item])

def count_dict(lst):
    d={}
    for item in set(lst):
        d[item]=count_item(item,lst)
    return d



#NA PLAYED MAGES
get_summoners=get_summoners()
get_matchlist=get_matchlist(get_summoners)
ingame_champions=ingame_champions(get_matchlist)
get_mages=get_mages()
ingame_mages=ingame_mages(ingame_champions,get_mages)
na_mages=count_dict(ingame_mages)


#EUW PLAYED MAGES
get_summoners2=get_summoners2()
get_matchlist2=get_matchlist2(get_summoners2)
ingame_champions2=ingame_champions2(get_matchlist2)
get_mages2=get_mages2()
ingame_mages2=ingame_mages2(ingame_champions2,get_mages2)
euw_mages=count_dict(ingame_mages2)



#Bar chart comparison of NA and EUW
width = 0.35
figure1=plt.bar(na_mages.keys(), na_mages.values(), -width, align='edge',color='orange',label='NA')
figure2=plt.bar(euw_mages.keys(), euw_mages.values(),+width, align='edge', color='red',label='EUW')

plt.xlabel("Mage Champions")
plt.ylabel("Frequency")
plt.xticks(rotation='vertical')
plt.legend()
plt.title("Comparison of Mages Played in NA and EUW ")
plt.show()


