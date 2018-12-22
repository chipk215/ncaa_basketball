from common_ratings import get_common_ratings
from pathlib import Path
import pandas as pd
import os


def drop_uncommon_ratings(df, common_list):
    drop_list = []
    ratings = list(df)
    for rating in ratings:
        if rating not in common_list:
            drop_list.append(rating)

    df.drop(columns=drop_list, inplace=True)
    return df


def run_main():
    common_list = get_common_ratings()
    print("Common Ratings: ")
    for item in common_list:
        print(item)

    season = 2003
    f_name = 'data/rankings_' + str(season) + '.csv'
    df_2003 = pd.read_csv(Path(f_name))
    df_combined = drop_uncommon_ratings(df_2003, common_list)

    for year in range(2004, 2019, 1):
        f_name = 'data/rankings_' + str(year) + '.csv'
        df = pd.read_csv(Path(f_name))
        df = drop_uncommon_ratings(df, common_list)
        df_combined = pd.concat([df_combined, df], join='inner')

    print("Combined shape: ", df_combined.shape)

    f_name = 'data/combined_seasons.csv'
    csv_file = Path(f_name)
    if csv_file.is_file():
        os.remove(csv_file)

    df_combined.to_csv(csv_file, sep=',', index=False)
    return


if __name__ == "__main__":
    run_main()
