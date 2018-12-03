import urllib
import pandas as pd
import common
from sqlalchemy import create_engine


def check_games_for_team(p_team, o_team, connection):
    season = 2015
    game_date = pd.Timestamp('2016-01-02 12:00:00')
    principal_result = common.get_games_for_team(season, p_team, game_date, connection)
    print(principal_result.shape)
    print(principal_result.head(principal_result.shape[0]))
    print(p_team +' Total Points', principal_result[['points_game']].sum(axis=0))

    opp_result = common.get_games_for_team(season, o_team, game_date, connection)
    print(opp_result.shape)
    print(opp_result.head(opp_result.shape[0]))
    print(o_team + ' Total Points', opp_result[['points_game']].sum(axis=0))

    return principal_result, opp_result


def check_process_game_record(connection):
    season = 2015
    game_date = pd.Timestamp('2016-01-02 12:00:00')
    principal = 'Oakland'
    opponent = 'Cleveland State'
    stats = common.process_game_record(season, game_date, principal, opponent, connection)
    print(stats.head())


def check_compute_feature_differences(connection):
    principal_df, opponent_df = check_games_for_team(connection)
    principal_vs_opponent = common.compute_feature_differences(principal_df, opponent_df)
    return principal_vs_opponent


def check_market_combine(connection):
    p_team = 'Oakland'
    o_team = 'Cleveland State'
    principal, opponent = check_games_for_team(p_team, o_team, connection)
    combined_principal = common.combine_market_data(principal, p_team)
    combined_opponent = common.combine_market_data(opponent, o_team)
    return combined_principal, combined_opponent


def run_stat_check():
    params = urllib.parse.quote_plus("DRIVER={SQL Server Native Client 11.0};"
                                     "SERVER=DESKTOP-LSOCJD8\SQLEXPRESS;"
                                     "DATABASE=NCAA_Basketball;"
                                     "Trusted_Connection=yes")

    engine = create_engine("mssql+pyodbc:///?odbc_connect={}".format(params))
    connection = engine.connect()

    # check_games_for_team('Oakland', 'Cleveland State',connection)
    # check_compute_feature_differences(connection)
    check_market_combine(connection)


if __name__ == "__main__":
    run_stat_check()
