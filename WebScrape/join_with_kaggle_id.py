from pathlib import Path
import pandas as pd
import os


def run_main():
    f_name = 'data/combined_seasons.csv'
    df_teams = pd.read_csv(Path(f_name))

    print(df_teams[df_teams.isnull().any(axis=1)])
    df_teams.dropna(inplace=True)
    f_ids = 'data/massey_school_names.csv'
    df_ids = pd.read_csv(Path(f_ids))
    df_ids.drop(columns=['kaggle_school'], inplace=True)

    result = pd.merge(df_teams, df_ids, left_on='Team', right_on='massey_school', how='left')
    print(result[result.isnull().any(axis=1)])
    result.dropna(inplace=True)
    result.drop(columns=['massey_school'], inplace=True)

    f_name = 'data/massey_seasons_with_id.csv'
    csv_file = Path(f_name)
    if csv_file.is_file():
        os.remove(csv_file)
    result.to_csv(csv_file, sep=',', index=False)

    return


if __name__ == "__main__":
    run_main()