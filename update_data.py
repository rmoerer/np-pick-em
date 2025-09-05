from pick_em.group import Group
import pandas as pd

current_year = 2025
group = Group(
    year=current_year,
    challenge_id=265, # have to figure this out by looking at the pick em json data
    group_id="f9ec66ba-415e-4cd9-bae5-6cb97aca226d"
)

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
