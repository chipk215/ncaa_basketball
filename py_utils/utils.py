import operator


# Compare the conferences of two teams playing in a game.
# If both teams are in power conference or both teams are not in a power conference return 0.
# If the opponent team is in a power conference and the first team is not in a power conference return -1
# If the first team is a power conference team and opponent is not then return 1.
def conf_compare(team_conf, opp_conf, top_tournament_conferences_list):
    team_top = team_conf in top_tournament_conferences_list
    opp_top = opp_conf in top_tournament_conferences_list
    if team_top == opp_top:
        return 0
    elif team_top :
        return 1
    else:
        return -1


def join_feature_name_with_importance_value(features, importances):
    """
    Join via a list of tuples, feature names with their importance values
    :param features: data frame whose features are represented by columns used by classifier
    :param importances: feature importance scores assigned by classifier
    :return: sorted list (highest importances first) of feature,importance tuples
    """
    if features.columns.shape[0] != importances.shape[0]:
        return []

    feature_importances = []
    for item in range(features.columns.shape[0]):
        feature_importances.append((features.columns[item], importances[item]))
    feature_importances_sorted = sorted(feature_importances, reverse=True, key=lambda kv: abs(kv[1]))

    return feature_importances_sorted


def display_important_features_rf_forest(classifier, features):
    importances = classifier.feature_importances_
    # print("Importances: ", importances)
    feature_importances = join_feature_name_with_importance_value(features, importances)
    print('Coefficient Values')
    for items in feature_importances:
        print(items[0], " ", items[1])


def get_tournament_record(df, season, round_, team):
    return df[(df['season_t'] == season) & (df['round'] == round_) & (df['team_t'] == team)]


def print_game_info(df, season, round_, team):
    stat_dict = {}

    upset_count = 0
    stat_count = 0
    t_rec = get_tournament_record(df, season, round_, team)
    opp_team = t_rec['team_o'].iloc[0]
    game_result = t_rec['game_result'].iloc[0]

    int_format_string = "{0:<20s}{1:15d}{2:>35d}{3:>15s}{4:>5s}"
    float_format_string = "{0:<20s}{1:17.2f}{2:>35.2f}{3:>13s}{4:>5s}"

    # stat name, high stat value is good, format of print string, stat alias, stat percent flag
    stat_list = [
        ('seed', False, int_format_string, 'Seed', False),
        ('SAG', False, float_format_string, 'SAG', False),
        ('WLK', False, float_format_string, 'WLK', False),
        ('WOL', False, float_format_string, 'WOL', False),
        ('RTH', False, float_format_string, 'RTH', False),
        ('COL', False, float_format_string, 'COL', False),
        ('POM', False, float_format_string, 'POM', False),
        ('DOL', False, float_format_string, 'DOL', False),
        ('RPI', False, float_format_string, 'RPI', False),
        ('MOR', False, float_format_string, 'MOR', False),
        ('opp_pts_avg', False, float_format_string, 'Allow PPG', False),
        ('allow_fg_pct', False, float_format_string, 'Allow FG %', True),
        ('allow_off_rebs_avg', False, float_format_string, 'Allow Off Rb Avg', False),
        ('allow_def_rebs_avg', False, float_format_string, 'Allow Def Rb Avg', False),
        ('allow_ft_att_avg', False, float_format_string, 'Allow FT ATT Avg', False),
        ('to_avg', False, float_format_string, 'Turnover Avg', False),
        ('SRS', True, float_format_string, 'SRS', False),
        ('pts_avg', True, float_format_string, 'PPG', False),
        ('poss_avg', True, float_format_string, 'Poss Avg', False),
        ('fg_pct', True, float_format_string, 'FG %', True),
        ('off_rebs_avg', True, float_format_string, 'Off Rb Avg', False),
        ('def_rebs_avg', True, float_format_string, 'Def Rb Avg', False),
        ('ft_att_avg', True, float_format_string, 'FT ATT Avg', False),
        ('ft_pct', True, float_format_string, 'FT %', True),
        ('steal_avg', True, float_format_string, 'Takeaway Avg', False),
        ('win_pct', True, float_format_string, 'Win %', True),
        ('off_rating', True, float_format_string, 'Off Rating', False)
    ]

    # print the table header
    print("{0:>45s}{1:>27s}{2:>15s}".format(team[0:25], opp_team[0:25], "Stat Upset"))

    for stat in stat_list:
        team_stat = stat[0] + '_t'
        opp_stat = stat[0] + '_o'
        stat_t = t_rec[team_stat].iloc[0]
        stat_o = t_rec[opp_stat].iloc[0]
        upset_flag = stat_upset(stat[1], stat_t, stat_o, game_result)

        if stat[4]:
            stat_t = 100 * stat_t
            stat_o = 100 * stat_o

        hint = "(L)"
        if stat[1]:
            hint = "(H)"

        print_string = stat[2].format(stat[3], stat_t, stat_o, str(upset_flag), hint)
        # print(print_string)
        stat_count = stat_count + 1
        if upset_flag:
            upset_count = upset_count + 1

        # save print data so i can be sorted
        stat_dict[print_string] = upset_flag

    # sort list by upset flag (True or False)
    sorted_dict = sorted(stat_dict.items(), key=operator.itemgetter(1), reverse=True)
    for k in sorted_dict:
        print(k[0])

    if t_rec['top_conf'].iloc[0] == 1:
        print('\n\nTop Conference= ', team)
    elif t_rec['top_conf'].iloc[0] == -1:
        print('\n\nTop Conference= ', opp_team)

    if t_rec['game_result'].iloc[0] == 1:
        print('\n', team, "Wins.")
    else:
        print('\n', opp_team, "Wins.")

    print('\nUpset Stat Count =', upset_count, ' out of', stat_count, ' stats.')
    return


def stat_upset(hi_stat_flag, stat_t, stat_o, game_result):
    if hi_stat_flag:
        upset_cond_1 = (game_result == 0) & (stat_t > stat_o)
        upset_cond_2 = (game_result == 1) & (stat_t < stat_o)
    else:
        upset_cond_1 = (game_result == 0) & (stat_t < stat_o)
        upset_cond_2 = (game_result == 1) & (stat_t > stat_o)

    return upset_cond_1 | upset_cond_2


def compute_percentage(x, tournament_games):
    # print(x)
    game_count = tournament_games[x[0]]
    # set_trace()
    val = 100.0 * len(x) / game_count

    return val

