import operator
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import pandas as pd
from sklearn import metrics
from sklearn.model_selection import train_test_split
from sklearn.metrics import log_loss
from sklearn.model_selection import cross_val_score


def display_confusion_matrix(y_test, y_pred):
    cnf_matrix = metrics.confusion_matrix(y_test, y_pred)
    class_names = [0, 1]
    fig, ax = plt.subplots()
    tick_marks = np.arange(len(class_names))
    plt.xticks(tick_marks, class_names)
    plt.yticks(tick_marks, class_names)
    # create heatmap
    sns.heatmap(pd.DataFrame(cnf_matrix), annot=True, cmap="YlGnBu", fmt='g')
    ax.xaxis.set_label_position("top")
    plt.tight_layout()
    plt.title('Confusion matrix', y=1.1)
    plt.ylabel('Actual label')
    plt.xlabel('Predicted label')
    return cnf_matrix


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


def display_important_features(important_features, features, display=1):
    feature_importances = join_feature_name_with_importance_value(features, important_features)
    if display:
        print('Coefficient Values')
        for items in feature_importances:
            print(items[0]," ", items[1])
    return feature_importances


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
        ('SOS', True, float_format_string, 'SOS', False),
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
    print("{0:>45s}{1:>27s}{2:>25s}".format(team[0:25], opp_team[0:25], "Stat Supports Winner"))

    for stat in stat_list:
        team_stat = stat[0] + '_t'
        opp_stat = stat[0] + '_o'
        stat_t = t_rec[team_stat].iloc[0]
        stat_o = t_rec[opp_stat].iloc[0]
        support_flag = supporting_stat(stat[1], stat_t, stat_o, game_result)

        if stat[4]:
            stat_t = 100 * stat_t
            stat_o = 100 * stat_o

        hint = "(L)"
        if stat[1]:
            hint = "(H)"

        print_string = stat[2].format(stat[3], stat_t, stat_o, str(support_flag), hint)
        # print(print_string)
        stat_count = stat_count + 1
        if support_flag:
            upset_count = upset_count + 1

        # save print data so it can be sorted
        stat_dict[print_string] = support_flag

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

    print('\nSupporting Stat Count=', upset_count, ' out of', stat_count, ' stats.')
    print('\n\n')
    return sorted_dict


def supporting_stat(hi_stat_flag, stat_t, stat_o, game_result):
    if hi_stat_flag:
        cond_1 = (game_result == -1) & (stat_t > stat_o)
        cond_2 = (game_result == 1) & (stat_t < stat_o)
    else:
        cond_1 = (game_result == -1) & (stat_t < stat_o)
        cond_2 = (game_result == 1) & (stat_t > stat_o)

    return not(cond_1 | cond_2)


def compute_percentage(x, tournament_games):
    # print(x)
    game_count = tournament_games[x[0]]
    # set_trace()
    val = 100.0 * len(x) / game_count

    return val


def get_hash_for_feature_labels(feature_list):
    join_string = '-'.join(feature_list)
    hash_value = hash(join_string)
    return hash_value


def save_model_stats(classifier, X, y, model_stats):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state= 5)
    classifier.fit(X_train, y_train)
    y_pred = classifier.predict(X_test)
    # save model stats
    prediction_probabilities = classifier.predict_proba(X_test)
    accuracy = metrics.accuracy_score(y_test, y_pred)
    precision = metrics.precision_score(y_test, y_pred)
    recall = metrics.recall_score(y_test, y_pred)
    log_loss_value = log_loss(y_test, prediction_probabilities)
    cross_val_scores = cross_val_score(classifier, X, y, cv=10, scoring='accuracy')
    cross_validation_average = cross_val_scores.mean()
    feature_labels = list(X_train)
    hash_value = get_hash_for_feature_labels(feature_labels)
    model_stats[hash_value] = {'accuracy': accuracy, 'precision': precision, 'recall': recall,
                               'log_loss': log_loss_value, 'cross_validation': cross_validation_average,
                               'labels': feature_labels}
    return model_stats


def negate_loser(x):
    if x == 0:
        x = -1
    return x


class Feature_Dictionary:
    def __init__(self):
        self.int_format_string = "{0:<20s}{1:15d}{2:>35d}{3:>15s}{4:>5s}"
        self.float_format_string = "{0:<20s}{1:17.2f}{2:>35.2f}{3:>13s}{4:>5s}"
        self.feature_dictionary = {
            #  name, stat evaluation function, format of print string, stat alias, stat percent flag
            'seed': ('LOW', self.int_format_string, 'Seed', False),
            'sag': ('LOW', self.float_format_string, 'SAG', False),
            'wlk': ('LOW', self.float_format_string, 'WLK', False),
            'wol': ('LOW', self.float_format_string, 'WOL', False),
            'rth': ('LOW', self.float_format_string, 'RTH', False),
            'col': ('LOW', self.float_format_string, 'COL', False),
            'pom': ('LOW', self.float_format_string, 'POM', False),
            'dol': ('LOW', self.float_format_string, 'DOL', False),
            'rpi': ('LOW', self.float_format_string, 'RPI', False),
            'mor': ('LOW', self.float_format_string, 'MOR', False),
            'opp_pts_avg': ('LOW', self.float_format_string, 'Allow PPG', False),
            'allow_fg_pct': ('LOW', self.float_format_string, 'Allow FG %', True),
            'allow_off_rebs_avg': ('LOW', self.float_format_string, 'Allow Off Rb Avg', False),
            'allow_def_rebs_avg': ('LOW', self.float_format_string, 'Allow Def Rb Avg', False),
            'allow_ft_att_avg': ('LOW', self.float_format_string, 'Allow FT ATT Avg', False),
            'to_avg': ('LOW', self.float_format_string, 'Turnover Avg', False),
            'to_net_avg': ('LOW', self.float_format_string, 'Net Turnover Avg', False),
            'srs': ('HIGH', self.float_format_string, 'SRS', False),
            'sos': ('HIGH', self.float_format_string, 'SOS', False),
            'pts_avg': ('HIGH', self.float_format_string, 'PPG', False),
            'poss_avg': ('HIGH', self.float_format_string, 'Poss Avg', False),
            'fg_pct': ('HIGH', self.float_format_string, 'FG %', True),
            'off_rebs_avg': ('HIGH', self.float_format_string, 'Off Rb Avg', False),
            'def_rebs_avg': ('HIGH', self.float_format_string, 'Def Rb Avg', False),
            'ft_att_avg': ('HIGH', self.float_format_string, 'FT ATT Avg', False),
            'ft_pct': ('HIGH', self.float_format_string, 'FT %', True),
            'steal_avg': ('HIGH', self.float_format_string, 'Takeaway Avg', False),
            'margin_victory_avg': ('HIGH', self.float_format_string, 'Margin Victory Avg', False),
            'win_pct': ('HIGH', self.float_format_string, 'Win %', True),
            'off_rating': ('HIGH', self.float_format_string, 'Off Rating', False)
        }

    @staticmethod
    def high_supporting_statistic(stat_t, stat_o, game_result):
        if game_result == -1:
            return stat_o > stat_t

        return stat_t > stat_o

    @staticmethod
    def low_supporting_statistic(stat_t, stat_o, game_result):
        if game_result == -1:
            return stat_o < stat_t
        return stat_t < stat_o

    def print_game_info(self, test_games, season, round_, team):
        stat_dict = {}
        supports_outcome_count = 0
        stat_count = 0
        game_record = get_tournament_record(test_games, season, round_, team)
        game_record = game_record.iloc[0]
        opp_team = game_record['team_o']
        game_result = game_record['game_result']

        # print the table header
        print("{0:>45s}{1:>27s}{2:>25s}".format(team[0:25], opp_team[0:25], "Stat Supports Winner"))

        for key, value in self.feature_dictionary.items():
            team_stat = key + '_t'
            opp_stat = key + '_o'
            stat_t = game_record[team_stat]
            stat_o = game_record[opp_stat]
            support_flag = self.does_feature_support_win(key, stat_t, stat_o, game_result)

            if value[3]:
                stat_t = 100 * stat_t
                stat_o = 100 * stat_o

            hint = "(L)"
            if value[0] == 'HIGH':
                hint = "(H)"

            print_string = value[1].format(value[2], stat_t, stat_o, str(support_flag), hint)
            stat_count += 1
            if support_flag:
                supports_outcome_count += 1

            stat_dict[print_string] = support_flag

        sorted_dict = sorted(stat_dict.items(), key=operator.itemgetter(1), reverse=True)
        for k in sorted_dict:
            print(k[0])

        if game_record['top_conf'] == 1:
            print('\n\nTop Conference= ', team)
        elif game_record['top_conf'] == -1:
            print('\n\nTop Conference= ', opp_team)

        if game_record['game_result'] == 1:
            print('\n', team, "Wins.")
        else:
            print('\n', opp_team, "Wins.")

        print('\nSupporting Stat Count=', supports_outcome_count, ' out of', stat_count, ' stats.')
        print('\n\n')

        return sorted_dict

    def does_feature_support_win(self, feature_label, stat_t, stat_o, game_result):
        if self.feature_dictionary[feature_label][0] == 'LOW':
            return self.low_supporting_statistic(stat_t, stat_o, game_result)
        else:
            return self.high_supporting_statistic(stat_t, stat_o, game_result)


def get_supporting_features(row, feature_dictionary, feature_list):
    supporting_features = []
    for feature in feature_list:
        if feature.startswith('delta_'):
            feature_name = feature[6:]
            feature_t = feature_name + '_t'
            feature_o = feature_name + '_o'
            if feature_dictionary.does_feature_support_win(feature_name,
                                                           row[feature_t],
                                                           row[feature_o],
                                                           row['game_result']):
                supporting_features.append(feature_name)
    return supporting_features


def hello():
    print("Hello")




