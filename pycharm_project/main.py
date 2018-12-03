import pandas as pd
import common
import db_utils


def run_main():
    # connect to the database
    connection = db_utils.connect_to_database()

    games_df = common.get_games_for_training(2015, connection)
    # games_df.info()

    stats = games_df.apply(lambda x: common.process_game_record(x.season, x.scheduled_date, x.market,
                                                                x.opp_market, connection), axis=1)

    game_stats_raw_df = stats[0]
    for row in range(1, stats.shape[0]):
        game_stats_raw_df = pd.concat([game_stats_raw_df, stats[row]], ignore_index=True)

    game_stats_raw_df['game_id'] = games_df['game_id']
    game_stats_raw_df['home_team'] = games_df['home_team']
    game_stats_raw_df['principal_team'] = games_df['market']
    game_stats_raw_df['opponent_team'] = games_df['opp_market']
    game_stats_raw_df['game_result'] = games_df['win'].astype(str)
    game_stats_raw_df['game_date'] = games_df['scheduled_date']
    game_stats_raw_df['principal_score'] = games_df['points_game']
    game_stats_raw_df['opponent_score'] = games_df['opp_points_game']
    # reorder columns

    column_titles = ['game_id', 'game_date', 'principal_team', 'opponent_team', 'home_team',
                     'principal_score', 'opponent_score', 'field_goals_pct',
                     'offensive_rebounds', 'free_throws_att', 'free_throws_pct',
                     'turnovers', 'win_pct', 'game_result']

    game_stats_raw_df = game_stats_raw_df.reindex(columns=column_titles)
    game_stats_raw_df.rename(columns={'field_goals_pct': 'delta_field_goals_pct',
                                      'offensive_rebounds': 'delta_avg_off_rebounds',
                                      'free_throws_att': 'delta_avg_free_throws_att',
                                      'free_throws_pct': 'delta_avg_free_throws_pct',
                                      'turnovers': 'delta_avg_turnovers',
                                      'win_pct': 'delta_win_pct'}, inplace=True)

    # encode all percentages to be between -1 < 0 < 1
    game_stats_raw_df.loc[:, ['delta_field_goals_pct', 'delta_avg_free_throws_pct']] /= 100.0
    encode_game_result = {"game_result": {"0": "LOSS", "1": "WIN"}}
    game_stats_raw_df.replace(encode_game_result, inplace=True)

    game_stats_df = game_stats_raw_df[abs(game_stats_raw_df.delta_win_pct) <= 1.000001]
    print(game_stats_df.shape)

    game_stats_df.to_csv('data\PARTIAL_D1_2015_Processed_Stats.csv', index=False)


if __name__ == "__main__":
    run_main()
