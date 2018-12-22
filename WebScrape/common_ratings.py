from pathlib import Path
import pandas as pd


def get_common_ratings():
    ignore_set = {'Rank'}
    common_ratings = set([])
    years = range(2003, 2019, 1)
    for year in years:
        # print("Processing ", year)
        f_name = 'data/rankings_' + str(year) + '.csv'
        csv_file = Path(f_name)
        df = pd.read_csv(csv_file)
        ratings = list(df)
        if len(common_ratings) == 0:
            common_ratings.update(set(ratings))
        else:
            common_ratings = common_ratings.intersection(set(ratings))

    common_list = []
    for rating in common_ratings:
        if rating not in ignore_set:
            common_list.append(rating)

    return common_list


def run_main():
    common_list = get_common_ratings()
    common_list.sort()
    print("\n\nRatings: \n")
    for item in common_list:
        print(item)
    return


if __name__ == "__main__":
    run_main()
