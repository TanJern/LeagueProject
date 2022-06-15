Purpose of project is to compare the mage champions used by players in two different regions.
NA and EUW are used as examples in code.

This work uses Riot-Watcher (https://github.com/pseudonym117/Riot-Watcher) as its API wrapper. 



Data used:<br />
-Top 12 ranked solo players from NA and EUW.<br />
-Any mage champions that appeared in each players' last 5 games ( a total of 60 games from each region).<br />


Issues:<br />
-Due to API limitations, the sample size of the data is small hence results may be highly variable and biased.<br />
-As data were only retreived from high ELO matches, the data(selected champions) is skewed.<br />


Instructions:<br />
-Please enter your Riot Development API Key before running code. <br />
https://developer.riotgames.com/ <br />
-my_region,player_region,and player_routing can be changed to compare data of other regions.<br />
-num_matches_data=5 can be edited to change the number of each players' past game.<br />
-Keyword "Mage" in get_Mage() and get_Mage2() can be swapped to "Tank", "Assassin" or other classes to view different comparisons.<br />

![Screenshot](example.png)
