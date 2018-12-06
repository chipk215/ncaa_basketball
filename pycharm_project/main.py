import pandas as pd
import common
import db_utils


def run_main():
    connection = db_utils.connect_to_database()
    games_df = common.get_games_for_training(2015, connection)
    combo_stats = games_df.apply(lambda x: common.get_team_stats(x.season, x.scheduled_date,
                                                                 x.market, x.opp_market,
                                                                 connection), axis=1)
    combo_df = combo_stats[0]
    for row in range(1, combo_stats.shape[0]):
        combo_df = pd.concat([combo_df, combo_stats[row]], ignore_index=True)

    combo_df.insert(0, 'game_id', games_df['game_id'])
    combo_df.insert(1, 'home_team', games_df['home_team'])
    combo_df.insert(2, 'principal_team', games_df['market'])
    combo_df.insert(3, 'opponent_team', games_df['opp_market'])
    combo_df.insert(4, 'game_result', games_df['win'].astype(str))
    combo_df.insert(5, 'game_date', games_df['scheduled_date'])
    combo_df.insert(6, 'principal_score', games_df['points_game'])
    combo_df.insert(7, 'opponent_score', games_df['opp_points_game'])

    # remove all records that have nan as win percentages
    combo_df = combo_df[(combo_df.prn_win_pct.notnull()) & (combo_df.opp_win_pct.notnull())]

    combo_df.to_csv('data\D1_2015_Combo_Stats.csv', index=False)
    return combo_df


if __name__ == "__main__":
    run_main()
