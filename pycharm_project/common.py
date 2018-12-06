import pandas as pd
import numpy as np


def compute_aggregate_stats(team_df):
    stats_df = team_df.drop(['scheduled_date', 'home_team', 'market', 'opp_market'], axis=1)

    # computed stats
    # number of game -> n = team_df.shape[0]
    # prn stats
    # avg points per game = points_game.sum() / n
    # fg pct = field_goals_made.sum() / field_goals_att.sum()
    # off rebounds per game = offensive_rebounds.sum() / n
    # ft attempts per game = free_throws_att.sum() / n
    # ft percentage = free_throws_made.sum()/ free_throws_att.sum()
    # turnovers per game = turnovers.sum() / n

    # sum all of the columns
    stats_df.loc['sum'] = stats_df.sum()
    n = stats_df.shape[0]
    prn_pts_avg = stats_df.at['sum', 'points_game'] / n
    prn_fg_pct = stats_df.at['sum', 'field_goals_made'] / stats_df.at['sum', 'field_goals_att']
    prn_off_rebs_avg = stats_df.at['sum', 'offensive_rebounds'] / n
    prn_ft_att_avg = stats_df.at['sum', 'free_throws_att'] / n
    prn_ft_pct = stats_df.at['sum', 'free_throws_made'] / stats_df.at['sum', 'free_throws_att']
    prn_turnover_avg = stats_df.at['sum', 'turnovers'] / n

    prn_allow_pts_avg = stats_df.at['sum', 'opp_points_game'] / n
    prn_allow_fg_pct = stats_df.at['sum', 'opp_field_goals_made'] / stats_df.at['sum', 'opp_field_goals_att']
    prn_allow_off_rebs_avg = stats_df.at['sum', 'opp_offensive_rebounds'] / n
    prn_allow_ft_att_avg = stats_df.at['sum', 'opp_free_throws_att'] / n
    prn_take_away_avg = stats_df.at['sum', 'opp_turnovers'] / n

    df_stats_dictionary = {'prn_pts_avg': [prn_pts_avg],
                           'prn_fg_pct': [prn_fg_pct],
                           'prn_off_rebs_avg': [prn_off_rebs_avg],
                           'prn_ft_att_avg': [prn_ft_att_avg],
                           'prn_ft_pct': [prn_ft_pct],
                           'prn_turnover_avg': [prn_turnover_avg],
                           'prn_win_pct': [np.nan],
                           'prn_allow_pts_avg': [prn_allow_pts_avg],
                           'prn_allow_fg_pct': [prn_allow_fg_pct],
                           'prn_allow_off_rebs_avg': [prn_allow_off_rebs_avg],
                           'prn_allow_ft_att_avg': [prn_allow_ft_att_avg],
                           'prn_take_away_avg': [prn_take_away_avg]
                           }

    results_df = pd.DataFrame(data=df_stats_dictionary, dtype=np.float32)

    if team_df.loc[0]['points_game'] > 0:
        results_df.loc[0, 'prn_win_pct'] = compute_win_percentage(team_df)

    return results_df


def combine_team_stats(principal_team_df, opp_team_df):

    combo_dict = {
        'prn_pts_avg': [principal_team_df.loc[0, 'prn_pts_avg']],
        'prn_fg_pct': [principal_team_df.loc[0, 'prn_fg_pct']],
        'prn_off_rebs_avg': [principal_team_df.loc[0, 'prn_off_rebs_avg']],
        'prn_ft_att_avg': [principal_team_df.loc[0, 'prn_ft_att_avg']],
        'prn_ft_pct': [principal_team_df.loc[0, 'prn_ft_pct']],
        'prn_turnover_avg': [principal_team_df.loc[0, 'prn_turnover_avg']],
        'prn_win_pct': [principal_team_df.loc[0, 'prn_win_pct']],
        'prn_allow_pts_avg': [principal_team_df.loc[0, 'prn_allow_pts_avg']],
        'prn_allow_fg_pct': [principal_team_df.loc[0, 'prn_allow_fg_pct']],
        'prn_allow_off_rebs_avg': [principal_team_df.loc[0, 'prn_allow_off_rebs_avg']],
        'prn_allow_ft_att_avg': [principal_team_df.loc[0, 'prn_allow_ft_att_avg']],
        'prn_take_away_avg': [principal_team_df.loc[0, 'prn_take_away_avg']],
        'opp_pts_avg': [opp_team_df.loc[0, 'prn_pts_avg']],
        'opp_fg_pct': [opp_team_df.loc[0, 'prn_fg_pct']],
        'opp_off_rebs_avg': [opp_team_df.loc[0, 'prn_off_rebs_avg']],
        'opp_ft_att_avg': [opp_team_df.loc[0, 'prn_ft_att_avg']],
        'opp_ft_pct': [opp_team_df.loc[0, 'prn_ft_pct']],
        'opp_turnover_avg': [opp_team_df.loc[0, 'prn_turnover_avg']],
        'opp_win_pct': [opp_team_df.loc[0, 'prn_win_pct']],
        'opp_allow_pts_avg': [opp_team_df.loc[0, 'prn_allow_pts_avg']],
        'opp_allow_fg_pct': [opp_team_df.loc[0, 'prn_allow_fg_pct']],
        'opp_allow_off_rebs_avg': [opp_team_df.loc[0, 'prn_allow_off_rebs_avg']],
        'opp_allow_ft_att_avg': [opp_team_df.loc[0, 'prn_allow_ft_att_avg']],
        'opp_take_away_avg': [opp_team_df.loc[0, 'prn_take_away_avg']]
    }

    combined_df = pd.DataFrame(data=combo_dict, dtype=np.float32)
    return combined_df


def get_team_stats(season, game_date, p_team, opp_team, connection):
    p_game_stats = get_team_stats_through_date(season, p_team, game_date, connection)
    p_summary_stats = compute_aggregate_stats(p_game_stats)

    opp_game_stats = get_team_stats_through_date(season, opp_team, game_date, connection)
    opp_summary_stats = compute_aggregate_stats(opp_game_stats)

    combined_df = combine_team_stats(p_summary_stats,  opp_summary_stats)
    return combined_df


def get_team_stats_through_date(season, team, game_date, db_connect) :
    print(team)
    team_search = team
    if "'" in team:
        pos = team.find("'")
        team_search = team[: pos]

    sql = """
        SELECT scheduled_date, home_team, market, opp_market, win, 
            points_game, opp_points_game,
            field_goals_att, opp_field_goals_att,
            field_goals_made, opp_field_goals_made,
            offensive_rebounds, opp_offensive_rebounds,
            free_throws_att, opp_free_throws_att,
            free_throws_made, opp_free_throws_made,
            turnovers , opp_turnovers     
        FROM [NCAA_Basketball].[dbo].[d1_2015_with_duplicates]
         WHERE (season = {}) AND (market like  N'{}') AND scheduled_date < '{}'
         """.format(season, team_search, game_date.strftime("%Y-%m-%d"))

    team_df = pd.read_sql_query(sql, db_connect)
    if team_df.shape[0] == 0:
        col_labels = list(team_df)
        data_values = [game_date, False, team, team, False,
                       0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                       0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        zero_series = pd.Series(data_values, index=col_labels)
        team_df = team_df.append(zero_series, ignore_index=True)

    return team_df


def get_games_for_training(season, db_connect):
    sql = """
               SELECT rows.game_id,  rows.season,  rows.scheduled_date, 
                    rows.home_team,  rows.market,  rows.opp_market,  rows.win, 
                    rows.points_game,  rows.opp_points_game    
               FROM (  
                 (SELECT *, RN=ROW_NUMBER() OVER(PARTITION BY game_id ORDER BY game_id) 
                 FROM [NCAA_Basketball].[dbo].[d1_2015_with_duplicates]) 
           ) AS rows 
               WHERE RN > 1 AND (season = {}) 
                """.format(season)

    games_df = pd.read_sql_query(sql, db_connect)
    return games_df


# Compute the win percentage for a team.
def compute_win_percentage(team_df):
    return team_df[team_df.win == True].count()['win']/team_df.shape[0]



