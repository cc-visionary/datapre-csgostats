# Data Analysis and Visualization for CSGO Players
## Data Dictionary
The data is located in the `./data/players.json` and stored as a json file with a `records` orientation.
### First 5 Data
<table>
<tr>
    <th>Index</th>
    <th>Competitive Rank</th>
    <th>Leaderboards Rank</th>
    <th>Username</th>
    <th>Primary Weapon</th>
    <th>Secondary Weapon</th>
    <th>K/D Score</th>
    <th>HS %</th>
    <th>Win Rate</th>
    <th>1vX</th>
    <th>Rating</th>
    <th>Kills</th>
    <th>Deaths</th>
</tr>
<tr>
    <td>0</td>
    <td>Silver I</td>
    <td>1</td>
    <td>Chosen 1</td>
    <td>m4a1_silencer</td>
    <td>ak47</td>
    <td>6.72</td>
    <td>33</td>
    <td>90</td>
    <td>12</td>
    <td>2.75</td>
    <td>195</td>
    <td>29</td>
</tr>
<tr>
    <td>1</td>
    <td>Silver I</td>
    <td>2</td>
    <td>David Hasslehof's Hairy Nuts</td>
    <td>ssg08</td>
    <td>ak47</td>
    <td>2.15</td>
    <td>65</td>
    <td>80</td>
    <td>11</td>
    <td>2.10</td>
    <td>277</td>
    <td>129</td>
</tr>
<tr>
    <td>2</td>
    <td>Silver I</td>
    <td>3</td>
    <td>樱岛麻衣</td>
    <td>ak47</td>
    <td>deagle</td>
    <td>2.36</td>
    <td>59</td>
    <td>10</td>
    <td>2</td>
    <td>1.99</td>
    <td>227</td>
    <td>96</td>
</tr>
<tr>
    <td>3</td>
    <td>Silver I</td>
    <td>4</td>
    <td>AdolfPootler</td>
    <td>ak47</td>
    <td>deagle</td>
    <td>1.73</td>
    <td>52</td>
    <td>50</td>
    <td>11</td>
    <td>1.98</td>
    <td>228</td>
    <td>132</td>
</tr>
<tr>
    <td>4</td>
    <td>Silver I</td>
    <td>5</td>
    <td>The Honse</td>
    <td>ak47</td>
    <td>revolver</td>
    <td>1.92</td>
    <td>52</td>
    <td>60</td>
    <td>7</td>
    <td>1.97</td>
    <td>265</td>
    <td>138</td>
</tr>
</table>

### Feature Description
<table>
<tr>
    <th>Column Name</th>
    <th>Type</th>
    <th>Description</th>
</tr>
<tr><td>Index</td><td>int</td><td>index of the data point in the dataset</td></tr>
<tr><td>Competitive Rank</td><td>string</td><td>in-game rank</td></tr>
<tr><td>Leaderboards Rank</td><td>int</td><td>ranking of player in the leaderboard for their in-game rank given their computed Rating</td></tr>
<tr><td>Username</td><td>string</td><td>display name of the player uses in-game, as of scraping</td></tr>
<tr><td>Primary Weapon</td><td>string</td><td>most used weapon</td></tr>
<tr><td>Secondary Weapon</td><td>string</td><td>second most used weapon</td></tr>
<tr><td>K/D Score</td><td>float</td><td>computed by dividing the amount of kills per death (Kills / Deaths)</td></tr>
<tr><td>HS %</td><td>int</td><td>percentage of kills that were made via headshot (shooting an enemy in the head)</td></tr>
<tr><td>Win Rate</td><td>int</td><td>win-to-loss ratio computed from the player's past 10 or more games</td></tr>
<tr><td>1vX</td><td>int</td><td>count of how many 1-versus-X situations has the player won in their past 10 games</td></tr>
<tr><td>Rating</td><td>float</td><td>computed performance overall rating of the player through **kills per round**, **rounds survived**, and **rounds with multiple kills**</td></tr>
<tr><td>Kills</td><td>int</td><td>pertain to enemy takedowns in-game</td></tr>
<tr><td>Deaths</td><td>int</td><td>amounts to the number of times a player dies in a match</td></tr>
</table>

## Questions 
1. What is the average KDR, winrate, and HS% of players in a given rank? 
2. What is the most used primary and secondary weapon?
3. What is the distribution of players in each rank?

## Other details
**Source**: [csgostats.gg](https://csgostats.gg)  
**Type of Analytics**: *Descriptive*  
**Methods applied**: *Group By*, *Aggregation*, and *Counting*   
