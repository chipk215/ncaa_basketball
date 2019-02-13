import pandas as pd
import itertools
from pathlib import Path


def get_id(team_name, team_data_df):
    team_record = team_data_df[team_data_df['team'] == team_name]
    team_id = team_record.iloc[0]['id']
    return team_id


def get_seed(team_name, team_data_df):
    team_record = team_data_df[team_data_df['team'] == team_name]
    team_seed = team_record.iloc[0]['seed']
    return team_seed


def get_quadrant(team_name, team_data_df):
    team_record = team_data_df[team_data_df['team'] == team_name]
    team_quad = team_record.iloc[0]['quadrant']
    return team_quad


def run_main():
    teams_file = "data/teams_2019.csv"
    team_data = pd.read_csv(Path(teams_file))
    # print(team_data.head())

    # games = list(itertools.combinations(team_data['team'], 2))
    games = list(itertools.combinations(team_data['team'], 2))
    print('Number of games= ', len(games))

    print(games[0])

    games_df = pd.DataFrame(games, columns=['team_t', 'team_o'])
    games_df['team_id_t'] = games_df.apply(lambda row: get_id(row['team_t'], team_data), axis=1)
    games_df['team_id_o'] = games_df.apply(lambda row: get_id(row['team_o'], team_data), axis=1)
    games_df['seed_t'] = games_df.apply(lambda row: get_seed(row['team_t'], team_data), axis=1)
    games_df['seed_o'] = games_df.apply(lambda row: get_seed(row['team_o'], team_data), axis=1)
    games_df['quad_t'] = games_df.apply(lambda row: get_quadrant(row['team_t'], team_data), axis=1)
    games_df['quad_o'] = games_df.apply(lambda row: get_quadrant(row['team_o'], team_data), axis=1)

    print(games_df.shape)


if __name__ == "__main__":
    run_main()
