import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import utils
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.ensemble import AdaBoostClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn import metrics


def read_summary_team_data():
    summary_data = pd.read_csv(Path('../data/sr_summaries_kaggle_id_no_opp.csv'))
    # drop opponent stat columns
    summary_data.drop(columns=['allow_fg_pct', 'allow_ft_att_avg', 'allow_off_rebs_avg',
                               'allow_def_rebs_avg'], inplace=True)

    summary_data.dropna(inplace=True)
    summary_data.rename(str.lower, axis='columns', inplace=True)
    return summary_data


def read_team_meta_data():
    teams = pd.read_csv(Path('../data/D1_teams.csv'))
    teams.drop(columns=['code_ncaa', 'school_ncaa', 'turner_name', 'league_name', 'league_alias', 'conf_alias',
                        'conf_id', 'division_name', 'division_alias', 'division_id',
                        'kaggle_team_id', 'venue_id'], inplace=True)

    teams.set_index('id', inplace=True)
    return teams


def read_tournament_results(tournament_season):
    tourney_data = pd.read_csv(Path('../data/tournament_results.csv'))
    tourney_data.drop(
        columns=['days_from_epoch', 'day', 'num_ot', 'academic_year', 'win_region', 'win_alias', 'lose_region',
                 'lose_alias', 'lose_code_ncaa', 'win_school_ncaa', 'win_code_ncaa', 'win_name', 'lose_name',
                 'win_pts', 'win_kaggle_team_id', 'lose_school_ncaa', 'lose_kaggle_team_id', 'lose_pts'], inplace=True)

    tourney_data = tourney_data[tourney_data['season'] >= tournament_season]
    return tourney_data


def join_tourney_team_data(tourney_data, teams):
    game_data = tourney_data.join(teams, on='win_team_id', how='left')
    game_data.rename(columns={'kaggle_team_id': 'win_kaggle_team_id', 'conf_name': 'win_conf_name'}, inplace=True)
    game_data = game_data.join(teams, on='lose_team_id', how='left')
    game_data.rename(columns={'kaggle_team_id': 'lose_kaggle_team_id', 'conf_name': 'lose_conf_name'}, inplace=True)
    return game_data


def recode_tourney_data(tourney_data):
    tourney_data['game_result'] = 1
    tourney_data.game_result = tourney_data.game_result.astype(int)
    tourney_data.rename(columns={"win_seed": "team_seed", "win_market": "team", "win_team_id": "team_id"}, inplace=True)
    tourney_data.rename(columns={"lose_seed": "opp_team_seed", "lose_market": "opp_team",
                                 "lose_team_id": "opp_team_id"}, inplace=True)

    tourney_data['start_season'] = tourney_data['season'] - 1

    # create some temporary buffer columns
    tourney_data['copy_team'] = tourney_data['team']
    tourney_data['copy_team_seed'] = tourney_data['team_seed']
    tourney_data['copy_team_id'] = tourney_data['team_id']

    # swap the team and opp team data
    tourney_data.loc[1::2, 'team'] = tourney_data.loc[1::2, 'opp_team']
    tourney_data.loc[1::2, 'opp_team'] = tourney_data.loc[1::2, 'copy_team']
    tourney_data.loc[1::2, 'team_seed'] = tourney_data.loc[1::2, 'opp_team_seed']
    tourney_data.loc[1::2, 'opp_team_seed'] = tourney_data.loc[1::2, 'copy_team_seed']
    tourney_data.loc[1::2, 'team_id'] = tourney_data.loc[1::2, 'opp_team_id']
    tourney_data.loc[1::2, 'opp_team_id'] = tourney_data.loc[1::2, 'copy_team_id']

    # flip the game result
    tourney_data.loc[1::2, 'game_result'] = 0

    # drop the temporary columns
    tourney_data.drop(columns=['copy_team', 'copy_team_seed', 'copy_team_id'], inplace=True)
    tourney_data.rename(columns={"team_seed": "seed_t", "opp_team_seed": "seed_o"}, inplace=True)

    tourney_data['Game Result'] = tourney_data.game_result.map({1: 'Win', 0: 'Lose'})

    return tourney_data


def merge_tourney_summary_data(tourney_data, summary_data):
    tourney_data = tourney_data.merge(summary_data, left_on=['start_season', 'team_id'],
                                      right_on=['season', 'team_id'], how='left', suffixes=('', '_y'))

    tourney_data.drop(columns=['season_y'], inplace=True)
    tourney_data = tourney_data.merge(summary_data, left_on=['start_season', 'opp_team_id'],
                                      right_on=['season', 'team_id'], how='left', suffixes=('_t', '_o'))

    tourney_data.drop(columns=['school_t', 'school_o', 'games_t', 'games_o', 'team_id_o'], inplace=True)

    return tourney_data


def join_tourney_team_data(tourney_data, teams):
    tourney_data = tourney_data.join(teams, on='team_id_t', how='left')
    tourney_data = tourney_data.join(teams, on='opp_team_id', how='left', lsuffix='_t', rsuffix='_o')
    tourney_data.rename(index=str, columns={'team': 'team_t', 'opp_team': 'team_o', 'opp_team_id': 'team_id_o'},
                        inplace=True)

    tourney_data['game_result'] = tourney_data.game_result.apply(utils.negate_loser)
    return tourney_data


def merge_tourney_ranking_data(tourney_data, computer_rankings):
    temp_merge = tourney_data.merge(computer_rankings, left_on=['season_t', 'team_id_t'],
                                    right_on=['season', 'kaggle_id'], how='left', suffixes=('', '_y'))

    temp_merge.drop(columns=['Team', 'season', 'win_pct', 'kaggle_id'], inplace=True)
    tourney_comp_ratings = temp_merge.merge(computer_rankings, left_on=['season_t', 'team_id_o'],
                                            right_on=['season', 'kaggle_id'], how='left', suffixes=('_t', '_o'))

    tourney_comp_ratings.drop(columns=['Team', 'season', 'win_pct', 'kaggle_id'], inplace=True)

    tourney_comp_ratings.rename(str.lower, axis='columns', inplace=True)
    return tourney_comp_ratings


def compute_delta_features(tourney_comp_ratings):
    tourney_comp_ratings['margin_victory_avg_t'] = tourney_comp_ratings['pts_avg_t'] - tourney_comp_ratings[
        'opp_pts_avg_t']
    tourney_comp_ratings['margin_victory_avg_o'] = tourney_comp_ratings['pts_avg_o'] - tourney_comp_ratings[
        'opp_pts_avg_o']

    tourney_comp_ratings['delta_margin_victory_avg'] = \
        tourney_comp_ratings['margin_victory_avg_t'] - tourney_comp_ratings['margin_victory_avg_o']

    tourney_comp_ratings['delta_fg_pct'] = tourney_comp_ratings['fg_pct_t'] - tourney_comp_ratings['fg_pct_o']

    tourney_comp_ratings['delta_off_rebs_avg'] = tourney_comp_ratings['off_rebs_avg_t'] - tourney_comp_ratings[
        'off_rebs_avg_o']

    tourney_comp_ratings['delta_def_rebs_avg'] = tourney_comp_ratings['def_rebs_avg_t'] - tourney_comp_ratings[
        'def_rebs_avg_o']

    tourney_comp_ratings['delta_ft_pct'] = tourney_comp_ratings['ft_pct_t'] - tourney_comp_ratings['ft_pct_o']

    tourney_comp_ratings['to_net_avg_t'] = tourney_comp_ratings['to_avg_t'] - tourney_comp_ratings['steal_avg_t']

    tourney_comp_ratings['to_net_avg_o'] = tourney_comp_ratings['to_avg_o'] - tourney_comp_ratings['steal_avg_o']

    tourney_comp_ratings['delta_to_net_avg'] = tourney_comp_ratings['to_net_avg_t'] - tourney_comp_ratings[
        'to_net_avg_o']

    tourney_comp_ratings['delta_win_pct'] = tourney_comp_ratings['win_pct_t'] - tourney_comp_ratings['win_pct_o']

    tourney_comp_ratings['delta_off_rating'] = tourney_comp_ratings['off_rating_t'] - tourney_comp_ratings[
        'off_rating_o']

    tourney_comp_ratings['delta_ft_att_avg'] = tourney_comp_ratings['ft_att_avg_t'] - tourney_comp_ratings[
        'ft_att_avg_o']

    tourney_comp_ratings['delta_seed'] = tourney_comp_ratings['seed_t'] - tourney_comp_ratings['seed_o']

    tourney_comp_ratings['delta_srs'] = tourney_comp_ratings['srs_t'] - tourney_comp_ratings['srs_o']
    tourney_comp_ratings['delta_sos'] = tourney_comp_ratings['sos_t'] - tourney_comp_ratings['sos_o']

    tourney_comp_ratings['delta_sag'] = tourney_comp_ratings['sag_t'] - tourney_comp_ratings['sag_o']
    tourney_comp_ratings['delta_wlk'] = tourney_comp_ratings['wlk_t'] - tourney_comp_ratings['wlk_o']
    tourney_comp_ratings['delta_wol'] = tourney_comp_ratings['wol_t'] - tourney_comp_ratings['wol_o']
    tourney_comp_ratings['delta_rth'] = tourney_comp_ratings['rth_t'] - tourney_comp_ratings['rth_o']
    tourney_comp_ratings['delta_col'] = tourney_comp_ratings['col_t'] - tourney_comp_ratings['col_o']
    tourney_comp_ratings['delta_pom'] = tourney_comp_ratings['pom_t'] - tourney_comp_ratings['pom_o']
    tourney_comp_ratings['delta_dol'] = tourney_comp_ratings['dol_t'] - tourney_comp_ratings['dol_o']
    tourney_comp_ratings['delta_rpi'] = tourney_comp_ratings['rpi_t'] - tourney_comp_ratings['rpi_o']
    tourney_comp_ratings['delta_mor'] = tourney_comp_ratings['mor_t'] - tourney_comp_ratings['mor_o']

    tourney_comp_ratings.drop(columns=['season_o'], inplace=True)
    tourney_comp_ratings.dropna(inplace=True)
    return tourney_comp_ratings


def run_main():
    tournament_season = 2003

    summary_data = read_summary_team_data()
    teams = read_team_meta_data()
    tourney_data = read_tournament_results(tournament_season)
    game_data = utils.compute_game_data(tourney_data, teams)

    computer_rankings = pd.read_csv(Path('../data/massey_seasons_with_id.csv'))
    computer_rankings = computer_rankings[computer_rankings['season'] >= tournament_season]

    tourney_data = recode_tourney_data(tourney_data)
    tourney_data = merge_tourney_summary_data(tourney_data, summary_data)
    tourney_data = join_tourney_team_data(tourney_data, teams)

    tourney_comp_ratings = merge_tourney_ranking_data(tourney_data, computer_rankings)
    tourney_comp_ratings = utils.implement_top_conference_feature(tourney_data, teams, game_data, tourney_comp_ratings)
    tourney_comp_ratings = utils.implement_seed_threshold_feature(tourney_comp_ratings)
    tourney_comp_ratings = compute_delta_features(tourney_comp_ratings)

    feature_data = tourney_comp_ratings.drop(
        columns=['round', 'game_date', 'seed_t', 'team_t', 'team_id_t', 'team_id_o',
                 'team_o', 'seed_o', 'team_id_o', 'game_result', 'start_season', 'game result',
                 'conf_name_t', 'conf_name_o']).copy()

    feature_data.drop(columns=['pts_avg_t', 'pts_avg_o', 'opp_pts_avg_t', 'opp_pts_avg_o',
                               'margin_victory_avg_t', 'margin_victory_avg_o',
                               'poss_avg_t', 'poss_avg_o',
                               'fg_pct_t', 'fg_pct_o',
                               'off_rebs_avg_t', 'off_rebs_avg_o', 'def_rebs_avg_t', 'def_rebs_avg_o',
                               'ft_pct_t', 'ft_pct_o',
                               'to_avg_t', 'to_avg_o', 'steal_avg_t', 'steal_avg_o',
                               'to_net_avg_t', 'to_net_avg_o',
                               'win_pct_t', 'win_pct_o', 'off_rating_t', 'off_rating_o',
                               'ft_att_avg_t', 'ft_att_avg_o', 'opp_pts_avg_t', 'opp_pts_avg_o',
                               'srs_t', 'srs_o', 'sos_t', 'sos_o',
                               'sag_t', 'sag_o', 'wlk_t', 'wlk_o', 'wol_t', 'wol_o',
                               'rth_t', 'rth_o', 'col_t', 'col_o', 'pom_t', 'pom_o',
                               'dol_t', 'dol_o', 'rpi_t', 'rpi_o', 'mor_t', 'mor_o'], inplace=True)

    # for now drop the delta seed features
    feature_data.drop(columns=['upset_seed_threshold'], inplace=True)

    X = feature_data[feature_data['season_t'] >= tournament_season]
    y = tourney_comp_ratings[tourney_comp_ratings['season_t'] >= tournament_season]['game_result']
    X = X.drop(columns=['season_t'])

    feature_list = list(X)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=5)

    number_estimators = 301
    bdt = AdaBoostClassifier(DecisionTreeClassifier(max_depth=1), algorithm="SAMME.R", n_estimators=number_estimators,
                             learning_rate=1)

    bdt.fit(X_train, y_train)
    score = bdt.score(X_train, y_train)
    print("Training Model Score= ", score)

    y_pred = bdt.predict(X_test)
    print("AdaBoost model accuracy is %2.2f" % metrics.accuracy_score(y_test, y_pred))

    prediction_probabilities = bdt.predict_proba(X_test)
    win_probabilities = pd.Series(prediction_probabilities[:, 1], index=X_test.index)
    predictions = pd.Series(y_pred, index=y_test.index)
    test_games = tourney_comp_ratings[tourney_comp_ratings.index.isin(X_test.index)].copy()

    test_games['predicted_result'] = predictions
    test_games['pred_win_prob'] = win_probabilities

    missed_predictions = test_games[test_games['game_result'] !=
                                    test_games['predicted_result']].sort_values(by='pred_win_prob', ascending=False)

    print("Missed predictions= ", missed_predictions.shape[0])

    feature_dictionary = utils.Feature_Dictionary()
    missed_predictions.apply(lambda x: feature_dictionary.print_game_info(test_games,
                                                                          x['season_t'],
                                                                          x['round'],
                                                                          x['team_t']), axis=1)

    supporting_features = missed_predictions.apply(
        lambda row: utils.get_supporting_features(row, feature_dictionary, feature_list),
        axis=1)

    missed_predictions = missed_predictions.merge(supporting_features.to_frame(name='supporting_features'), how='left',
                                                  left_index=True, right_index=True)

    missed_predictions['features'] = 100 * missed_predictions['supporting_features'].apply(lambda x: len(x)) / len(
        feature_list)

    missed_predictions['game_index'] = missed_predictions.index

    plot_missed_predictions_df = missed_predictions[['game_index', 'features']]
    plot_missed_predictions_df = pd.melt(plot_missed_predictions_df, id_vars='game_index',
                                         var_name='Features Supporting Outcome')
    # plot_missed_predictions_df.head()
    # m_plot = sns.barplot(x='game_index', y='value', hue='Features Supporting Outcome', data=plot_missed_predictions_df)
    # plt.title("Percentage Of Features Consistent With Incorrectly Predicted Game Outcomes")
    # plt.ylabel('Percentage')
    # plt.xlabel('Game Index')
    # m_plot.figure.set_size_inches(20, 6)

    print("Missed Predictions with greater than 50% feature support")
    print(plot_missed_predictions_df[plot_missed_predictions_df['value'] > 50])

    # analyze game index 417
    print(missed_predictions.loc[417])
    missed_game = X.loc[417].to_frame().T

    staged_predictions = bdt.staged_predict(missed_game)

    class_team_votes = 0
    class_opp_votes = 0

    estimator_stubs = []
    for stub_estimator in bdt.estimators_:
        stub_tree = stub_estimator.tree_
        stub_feature_index = stub_tree.feature[0]
        stub_feature = missed_game.columns[stub_feature_index]
        threshold_value = stub_tree.threshold[0]
        test_value = missed_game.iloc[0, stub_feature_index]
        left_child_node = stub_tree.children_left[0]
        left_values = stub_tree.value[left_child_node][0]
        right_child_node = stub_tree.children_right[0]
        right_values = stub_tree.value[right_child_node][0]
        node_samples = stub_tree.n_node_samples
        test_string = "Test: {0} ({1:6.3f}) <= {2:6.3f}".format(stub_feature, test_value, threshold_value)
        left_string = "Left: Samples= {0},  Percent Split= {1:5.3f}, {2:5.3f}".format(node_samples[left_child_node],
                                                                                      left_values[0], left_values[1])

        right_string = "Right: Samples= {0},  Percent Split= {1:5.3f}, {2:5.3f}".format(node_samples[right_child_node],
                                                                                        right_values[0], right_values[1])

        if test_value <= threshold_value:
            # choose left node
            if left_values[0] >= left_values[1]:
                result_string = "Result: Left --> Choose Class -1"
                class_opp_votes += 1
            else:
                result_string = "Result: Left --> Choose Class 1"
                class_team_votes +=1
        else:
            # choose right node
            if right_values[0] >= right_values[1]:
                result_string = "Result: Right --> Choose Class -1"
                class_opp_votes += 1
            else:
                result_string = "Result: Right --> Choose Class 1"
                class_team_votes += 1

        if next(staged_predictions) == 1:
            staged_prediction_string = 'Stage Prediction= Class 1'
        else:
            staged_prediction_string = 'Stage Prediction= Class -1'

        stub_dict = {
            'test_string': test_string,
            'left_string': left_string,
            'right_string': right_string,
            'result_string': result_string,
            'staged_prediction_string': staged_prediction_string
        }
        estimator_stubs.append(stub_dict)

    item_count = 0
    for item in estimator_stubs:
        print("Estimator: ",item_count)
        print(item['test_string'])
        print(item['left_string'])
        print(item['right_string'])
        print(item['result_string'])
        print(item['staged_prediction_string'])
        print("-----------")
        item_count += 1

    print("Class Team Votes= ", class_team_votes)
    print("Class Opp Votes= ", class_opp_votes)
    return


if __name__ == "__main__":
    run_main()
