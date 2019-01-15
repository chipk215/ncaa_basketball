import pandas as pd
from pathlib import Path


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
    #tourney_data.drop(
    #    columns=['days_from_epoch', 'day', 'num_ot', 'academic_year', 'win_region', 'win_alias', 'lose_region',
    #             'lose_alias', 'lose_code_ncaa', 'win_school_ncaa', 'win_code_ncaa', 'win_name', 'lose_name',
    #             'win_pts', 'win_kaggle_team_id', 'lose_school_ncaa', 'lose_kaggle_team_id', 'lose_pts'], inplace=True)

    tourney_data = tourney_data[tourney_data['season'] >= tournament_season]
    return tourney_data
