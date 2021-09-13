from pick_em.group import Group
import pandas as pd

current_year = 2021
group = Group(current_year, "22663954-fbb6-3948-b2e9-d96e7b0eae19")

current_week = group.week

# save all games up to the current week
games_list = []
for week in range(current_week):
    games_list.extend(group.get_week_games(week+1))
df = pd.DataFrame(games_list)
df.to_csv("data/games_%i.csv" % current_year)

# save all publicly available picks for all entries
picks_list = []
for entry in group.entries:
    picks_list.extend(entry.all_picks())
df2 = pd.DataFrame(picks_list)
df2.to_csv("data/picks_%i.csv" % current_year)
