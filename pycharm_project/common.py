import pandas as pd


def get_games_for_training(season, db_connect):
    sql = ("\n"
           "    SELECT TOP 300 game_id, season, scheduled_date, \n"
           "        home_team, market, opp_market, win, \n"
           "        points_game, opp_points_game,\n"
           "        field_goals_pct, \n"
           "        offensive_rebounds, \n"
           "        free_throws_att,\n"
           "        free_throws_pct,\n"
           "        turnovers      \n"
           "    FROM [NCAA_Basketball].[dbo].[d1_2015]\n"
           "    WHERE (season = {}) \n"
           "     ").format(season)

    games_df = pd.read_sql_query(sql, db_connect)
    return games_df


# Notes
# The database assigns labels to teams in a game. One team is labeled as 'market' while the other team
# is labeled as 'opp_market'. When gathering games for a specific team both fields must be searched.
def get_games_for_team(season, team, game_date, db_connect):
    team_search = team
    if "'" in team:
        pos = team.find("'")
        team_search = team[: pos]
        print(team)

    sql = """
    SELECT scheduled_date, home_team, market, opp_market, win, 
        points_game, opp_points_game,
        field_goals_pct, opp_field_goals_pct,
        offensive_rebounds, opp_offensive_rebounds,
        free_throws_att, opp_free_throws_att,
        free_throws_pct, opp_free_throws_pct,
        turnovers , opp_turnovers     
    FROM [NCAA_Basketball].[dbo].[d1_2015]
     WHERE (season = {}) AND ((market like  N'{}') OR (opp_market like  N'{}') ) AND scheduled_date < '{}'
     """.format(season, team_search, team_search, game_date.strftime("%Y-%m-%d"))

    team_df = pd.read_sql_query(sql, db_connect)
    if team_df.shape[0] == 0:
        col_labels = list(team_df)
        data_values = [game_date, False, team, team, False, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                       0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        zero_series = pd.Series(data_values, index=col_labels)
        team_df = team_df.append(zero_series, ignore_index=True)

    return team_df


# Compute the win percentage for a team.
def compute_win_percentage(team_df):
    return team_df[team_df.win == True].count()['win']/team_df.shape[0]


# Extract the team data categorized as 'market' and the team data
#  categorized as 'opp_market'
# Change the boolean sense of the win column for the opp_market data
# to correspond to market data
# Rename the opp_market column labels to match the market labels and
# combine the two data frames into a single data frame
def combine_market_data(df, team):

    label_dict = {'opp_market': 'market',
                  'opp_points_game': 'points_game',
                  'opp_field_goals_pct': 'field_goals_pct',
                  'opp_offensive_rebounds': 'offensive_rebounds',
                  'opp_free_throws_att': 'free_throws_att',
                  'opp_free_throws_pct': 'free_throws_pct',
                  'opp_turnovers': 'turnovers'}

    market_df = df.loc[df['market'] == team, ['scheduled_date', 'home_team', 'market',
                                              'win', 'points_game', 'field_goals_pct',
                                              'offensive_rebounds', 'free_throws_att',
                                              'free_throws_pct', 'turnovers']]

    opp_market_df = df.loc[df['opp_market'] == team, ['scheduled_date', 'home_team', 'opp_market',
                                                      'win', 'opp_points_game', 'opp_field_goals_pct',
                                                      'opp_offensive_rebounds', 'opp_free_throws_att',
                                                      'opp_free_throws_pct', 'opp_turnovers']]

    # complement the win and home columns in the opp_market df
    opp_market_df.win = ~opp_market_df.win.astype('bool')
    opp_market_df.home_team = ~opp_market_df.home_team.astype('bool')

    # change the labels in the opp_market
    opp_market_df.rename(columns=label_dict, inplace=True)

    combined_df = market_df.append(opp_market_df, ignore_index=True)
    return combined_df


def process_game_record(season, game_date, principal_team, opp_team, connection):
    # These two data frames contain all the games the corresponding team has played
    # prior to the specified game date. In each data frame the team my be listed as
    # either the 'market' team or the 'opp_market' team. The market data needs to be combined.
    principal_df = get_games_for_team(season, principal_team, game_date, connection)
    opponent_df = get_games_for_team(season, opp_team, game_date, connection)

    combined_principal = combine_market_data(principal_df, principal_team)
    combined_opponent = combine_market_data(opponent_df, opp_team)

    result = compute_feature_differences(combined_principal, combined_opponent)
    return result


def compute_feature_differences(principal_df, opponent_df):

    principal_summary = principal_df.describe()
    opponent_summary = opponent_df.describe()

    # if this is the first game for either team return 0s as the differences in stats
    # The win_diff value of -1000.0 is used to indicate the record should be deleted
    # since there was no game history for the team prior to the specified date
    if principal_df.loc[0]['points_game'] == 0:
        diff = principal_summary.loc['mean'] - principal_summary.loc['mean']
        win_diff = -1000.0
    elif opponent_df.loc[0]['points_game'] == 0:
        diff = opponent_summary.loc['mean'] - opponent_summary.loc['mean']
        win_diff = -1000.0
    else:
        win_diff = compute_win_percentage(principal_df) - compute_win_percentage(opponent_df)
        diff = principal_summary.loc['mean'] - opponent_summary.loc['mean']

    principal_vs_opponent = diff.to_frame(name="Difference").transpose()
    principal_vs_opponent['win_pct'] = pd.Series(win_diff, index=principal_vs_opponent.index)

    return principal_vs_opponent
