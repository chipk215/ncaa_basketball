import common
import db_utils
import pandas as pd


def get_games_for_training_test(connection):
    season = 2015
    games_df = common.get_games_for_training(season, connection)
    return games_df


def get_stats_for_team_test(team, connection):
    game_stats = get_team_season_stats_through_date_test(team, connection)
    summary_stats = common.compute_aggregate_stats(game_stats)
    return summary_stats


def get_team_season_stats_through_date_test(team, connection):
    season = 2015
    game_date = pd.Timestamp('2016-01-02 12:00:00')
    game_stats = common.get_team_stats_through_date(season,  team, game_date, connection)
    print(game_stats.head())
    return game_stats


def combine_team_stats_test(connection):
    p_team = get_stats_for_team_test('Virginia Tech', connection)
    o_team = get_stats_for_team_test('Notre Dame', connection)
    combined_df = common.combine_team_stats(p_team, o_team)
    return combined_df


def run_main():
    connection = db_utils.connect_to_database()
    # get_games_for_training_test(connection)
    # get_stats_for_team_test('Oakland', connection)
    combine_team_stats_test(connection)


if __name__ == "__main__":
    run_main()
