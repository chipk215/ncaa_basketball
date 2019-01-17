import pandas as pd
from pathlib import Path
import utils


def read_summary_team_data(f_name):
    summary_data = pd.read_csv(Path(f_name))
    # drop opponent stat columns
    summary_data.drop(columns=['allow_fg_pct', 'allow_ft_att_avg', 'allow_off_rebs_avg',
                               'allow_def_rebs_avg'], inplace=True)

    summary_data.dropna(inplace=True)
    summary_data.rename(str.lower, axis='columns', inplace=True)
    return summary_data


def read_team_meta_data(f_name):
    teams = pd.read_csv(Path(f_name))
    teams.drop(columns=['code_ncaa', 'school_ncaa', 'turner_name', 'league_name', 'league_alias', 'conf_alias',
                        'conf_id', 'division_name', 'division_alias', 'division_id',
                        'kaggle_team_id', 'venue_id'], inplace=True)

    teams.set_index('id', inplace=True)
    return teams


def read_tournament_results(f_name, tournament_season):
    tourney_data = pd.read_csv(Path(f_name))
    # tourney_data.drop(
    #    columns=['days_from_epoch', 'day', 'num_ot', 'academic_year', 'win_region', 'win_alias', 'lose_region',
    #             'lose_alias', 'lose_code_ncaa', 'win_school_ncaa', 'win_code_ncaa', 'win_name', 'lose_name',
    #             'win_pts', 'win_kaggle_team_id', 'lose_school_ncaa', 'lose_kaggle_team_id', 'lose_pts'], inplace=True)

    tourney_data = tourney_data[tourney_data['season'] >= tournament_season]
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
