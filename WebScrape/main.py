from bs4 import BeautifulSoup
import requests
from io import StringIO
import pandas as pd
import os
from pathlib import Path


url_dict = {
    2018: "https://www.masseyratings.com/cb/arch/compare2018-18.htm",
    2017: "https://www.masseyratings.com/cb/arch/compare2017-18.htm",
    2016: "https://www.masseyratings.com/cb/arch/compare2016-18.htm",
    2015: "https://www.masseyratings.com/cb/arch/compare2015-18.htm",
    2014: "https://www.masseyratings.com/cb/arch/compare2014-19.htm",
    2013: "https://www.masseyratings.com/cb/arch/compare2013-19.htm",
    2012: "https://www.masseyratings.com/cb/arch/compare2012-18.htm",
    2011: "https://www.masseyratings.com/cb/arch/compare2011-18.htm",
    2010: "https://www.masseyratings.com/cb/arch/compare2010-18.htm",
    2009: "https://www.masseyratings.com/cb/arch/compare2009-18.htm",
    2008: "https://www.masseyratings.com/cb/arch/compare2008-18.htm",
    2007: "https://www.masseyratings.com/cb/arch/compare2007-18.htm",
    2006: "https://www.masseyratings.com/cb/arch/compare2006-18.htm",
    2005: "https://www.masseyratings.com/cb/arch/compare2005-18.htm",
    2004: "https://www.masseyratings.com/cb/arch/compare2004-17.htm",
    2003: "https://www.masseyratings.com/cb/arch/compare2003-14.htm"
}

width_dict = {
    2018: [3, 4, 4, 4, 4, 6, 4, 4, 4, 4,
           5, 18, 4, 7, 6, 4, 4, 4, 4, 6,
           4, 4, 4, 4, 6, 4, 4, 4, 4, 5,
           11, 4, 4, 4, 4, 4, 6, 4, 4, 4,
           4, 6, 4, 4, 4, 4, 5, 11, 4, 4,
           4, 4, 4, 6, 4, 4, 4, 4, 6, 4,
           4, 4, 4, 5, 11, 4, 4, 4, 4, 4,
           6, 4, 4, 4, 4, 6, 4, 4, 8, 7,
           7],
    2017: [3, 4, 4, 4, 4, 6, 4, 4, 4, 4,
           5, 18, 4, 7, 6, 4, 4, 4, 4, 6,
           4, 4, 4, 4, 6, 4, 4, 4, 4, 5,
           11, 4, 4, 4, 4, 4, 6, 4, 4, 4,
           4, 6, 4, 4, 4, 4, 5, 11, 4, 4,
           4, 4, 4, 6, 4, 4, 4, 4, 6, 4,
           4, 4, 4, 5, 11, 5, 4, 4, 4, 4,
           6, 4, 4, 4, 4, 6, 4, 4, 4, 4,
           4, 11, 4, 4, 4, 4, 4, 8, 7, 7],
    2016: [3, 4, 4, 4, 4, 6, 4, 4, 4, 4,
           5, 18, 4, 7, 6, 4, 4, 4, 4, 6,
           4, 4, 4, 4, 6, 4, 4, 4, 4, 5,
           11, 4, 4, 4, 4, 4, 6, 4, 4, 4,
           4, 6, 4, 4, 4, 4, 5, 11, 4, 4,
           4, 4, 4, 6, 4, 4, 4, 4, 6, 4,
           4, 4, 4, 5, 11, 5, 4, 4, 4, 4,
           6, 4, 8, 7, 7],
    2015: [3, 4, 4, 4, 4, 6, 4, 4, 4, 4,
           5, 17, 6, 7, 6, 4, 4, 4, 4, 6,
           4, 4, 4, 4, 6, 4, 4, 4, 4, 5,
           11, 4, 4, 4, 4, 4, 6, 4, 4, 4,
           4, 6, 4, 4, 4, 4, 5, 11, 4, 4,
           4, 4, 4, 6, 4, 4, 4, 4, 6, 4,
           4, 4, 4, 5, 11, 5, 4, 4, 4, 4,
           6, 4, 8, 7, 7],
    2014: [3, 4, 4, 4, 4, 6, 4, 4, 4, 4,
           5, 17, 6, 7, 6, 4, 4, 4, 4, 6,
           4, 4, 4, 4, 6, 4, 4, 4, 4, 5,
           11, 4, 4, 4, 4, 4, 6, 4, 4, 4,
           4, 6, 4, 4, 4, 4, 5, 11, 4, 4,
           4, 4, 4, 6, 4, 4, 4, 4, 6, 4,
           4, 4, 4, 5, 11, 4, 4, 4, 4, 4,
           6, 4, 4, 4, 4, 8, 7, 7],
    2013: [3, 4, 4, 4, 4, 6, 4, 4, 4, 4,
           5, 17, 6, 7, 6, 4, 4, 4, 4, 6,
           4, 4, 4, 4, 6, 4, 4, 4, 4, 5,
           11, 4, 4, 4, 4, 4, 6, 4, 4, 4,
           4, 6, 4, 4, 4, 4, 5, 11, 4, 4,
           4, 4, 4, 6, 4, 4, 4, 4, 6, 4,
           4, 4, 4, 5, 11, 4, 4, 4, 4, 4,
           5, 8, 7, 7],
    2012: [3, 4, 4, 4, 4, 6, 4, 4, 4, 4,
           5, 17, 6, 7, 6, 4, 4, 4, 4, 6,
           4, 4, 4, 4, 6, 4, 4, 4, 4, 5,
           11, 4, 4, 4, 4, 4, 6, 4, 4, 4,
           4, 6, 4, 4, 4, 4, 5, 11, 4, 4,
           4, 4, 4, 6, 4, 4, 4, 4, 6, 4,
           4, 4, 4, 5, 11, 4, 4, 4, 4, 4,
           5, 8, 7, 7],
    2011: [3, 4, 4, 4, 4, 6, 4, 4, 4, 4,
           5, 17, 6, 7, 6, 4, 4, 4, 4, 6,
           4, 4, 4, 4, 6, 4, 4, 4, 4, 5,
           11, 4, 4, 4, 4, 4, 6, 4, 4, 4,
           4, 6, 4, 4, 4, 4, 5, 11, 4, 4,
           4, 4, 4, 5, 4, 4, 4, 4, 6, 4,
           8, 7, 7],
    2010: [3, 4, 4, 4, 4, 6, 4, 4, 4, 4,
           5, 17, 6, 7, 6, 4, 4, 4, 4, 6,
           4, 4, 4, 4, 6, 4, 4, 4, 4, 5,
           11, 4, 4, 4, 4, 4, 6, 4, 4, 4,
           4, 6, 4, 4, 4, 4, 5, 11, 4, 4,
           4, 4, 4, 5, 4, 4, 4, 4, 6, 4,
           8, 7, 7],
    2009: [3, 4, 4, 4, 4, 6, 4, 4, 4, 4,
           5, 17, 6, 5, 4, 4, 4, 4, 6, 4,
           4, 4, 4, 6, 4, 4, 4, 4, 5, 11,
           4, 4, 4, 4, 4, 6, 4, 4, 4, 4,
           6, 4, 4, 4, 4, 5, 11, 4, 4, 4,
           4, 4, 8, 7, 7],
    2008: [3, 4, 4, 4, 4, 6, 4, 4, 4, 4,
           5, 17, 6, 5, 4, 4, 4, 4, 6, 4,
           4, 4, 4, 6, 4, 4, 4, 4, 5, 11,
           4, 4, 4, 4, 4, 6, 4, 4, 4, 4,
           6, 4, 4, 4, 4, 5, 11, 4, 4, 4,
           4, 8, 7, 7],
    2007: [3, 4, 4, 4, 4, 6, 4, 4, 4, 4,
           5, 17, 6, 5, 4, 4, 4, 4, 6, 4,
           4, 4, 4, 6, 4, 4, 4, 4, 5, 11,
           4, 4, 4, 4, 4, 6, 4, 4, 4, 4,
           6, 4, 4, 4, 4, 5, 11, 4, 4, 8,
           7, 7],
    2006: [3, 4, 4, 4, 4, 6, 4, 4, 4, 4,
           5, 17, 6, 5, 4, 4, 4, 4, 6, 4,
           4, 4, 4, 6, 4, 4, 4, 4, 5, 11,
           4, 4, 4, 4, 4, 6, 4, 4, 4, 4,
           6, 4, 8, 7, 7],
    2005: [3, 4, 4, 4, 4, 6, 4, 4, 4, 4,
           5, 17, 6, 5, 4, 4, 4, 4, 6, 4,
           4, 4, 4, 6, 4, 4, 4, 4, 5, 11,
           4, 4, 4, 4, 4, 6, 4, 4, 4, 6,
           4, 4, 4, 7, 5, 7, 7],
    2004: [3, 4, 4, 4, 4, 6, 4, 4, 4, 4,
           5, 17, 6, 5, 4, 4, 4, 4, 6, 4,
           4, 4, 4, 6, 4, 4, 4, 4, 5, 11,
           4, 4, 4, 4, 4, 6, 4, 4, 4, 6,
           6, 7, 7, 7],
    2003: [3, 4, 4, 4, 4, 6, 4, 4, 4, 4,
           5, 17, 6, 5, 4, 4, 4, 4, 6, 4,
           4, 4, 4, 6, 4, 4, 4, 4, 5, 11,
           4, 4, 4, 4, 4, 6, 4, 4, 4, 8,
           7, 7]
}

start_text_dict = {
    2018: 'WLK BWE',
    2017: 'BWE WLK',
    2016: 'BWE FAS',
    2015: 'STF DII',
    2014: 'STH STF',
    2013: 'KPK STH',
    2012: 'KPK BOB',
    2011: 'KPK SAG',
    2010: 'MAS SAG',
    2009: 'BOB GRN',
    2008: 'GRN BOB',
    2007: 'ROH SEL',
    2006: 'BOB GRN',
    2005: 'BOB ROH',
    2004: 'WLK MAS',
    2003: 'SAG BOB'
}


def make_csv_line(line):
    no_comma = line.lstrip(' ').replace(',', '')
    words = no_comma.split()
    stripped_words = []
    for word in words:
        stripped_words.append(word.strip())
    return ','.join(stripped_words)


def compute_win_percentage(team_record):
    components = team_record.split('-')
    return float(int(components[0]))/(int(components[0]) + int(components[1]))


def run_main():
    season = 2003

    source = requests.get(url_dict[season]).text
    soup = BeautifulSoup(source, 'lxml')

    pre = soup.find('pre')

    start_section_text = start_text_dict[season]
    end_section_text = '--------------------'

    page_text = pre.text.strip()
    start_position = page_text.find(start_section_text)
    end_position = page_text.find(end_section_text)

    table_text = page_text[start_position:end_position]

    lines = table_text.splitlines()

    first_row_copied = False
    result = []
    for line in lines:
        # handle blank lines
        if not line:
            # blank line do not copy into result
            continue
        elif line.lstrip(' ').startswith(start_section_text):
            if not first_row_copied:
                result.append(make_csv_line(line))
                first_row_copied = True
            else:
                continue
        else:
            # not a blank line or a column header
            result.append(line[1:])

    print(len(result))

    # Rename all the occurrences of Rank and Team columns except for the first pair

    # split the words in the line into a list
    column_names = result[0].split(',')
    rank_indices = [i for i, column in enumerate(column_names) if column == 'Rank']
    rank_indices = rank_indices[1:]

    for i in range(1, len(rank_indices)+1):
        str_index = str(i)
        column_names[rank_indices[i-1]] = 'Rank_' + str_index
        column_names[rank_indices[i-1] + 1] = 'Team_' + str_index

    string_buffer = ''
    for line in result[1:]:
        string_buffer = string_buffer + line + "\n"

    # len(width_dict[season])
    df = pd.read_fwf(StringIO(string_buffer), widths=width_dict[season], names=column_names,
                     usecols=column_names[:42])

    df['season'] = season

    df['win_pct'] = df.apply(lambda row: compute_win_percentage(row.Record), axis=1)

    drop_cols_2018 = ['Record', 'Rank_1', 'Team_1', 'Rank_2', 'Team_2', 'Rank_3', 'Team_3', 'BNT',
                      'USA', 'AP', 'DES', 'Mean', 'Median', 'St.Dev']

    drop_cols_2017 = ['Record', 'Rank_1', 'Team_1', 'Rank_2', 'Team_2', 'Rank_3', 'Team_3', 'Rank_4', 'Team_4',
                      'USA', 'AP', 'DES', 'Mean', 'Median', 'St.Dev']

    drop_cols_2016 = ['Record', 'Rank_1', 'Team_1', 'Rank_2', 'Team_2', 'Rank_3', 'Team_3', 'D1A',
                      'USA', 'AP', 'DES', 'Mean', 'Median', 'St.Dev']

    drop_cols_2015 = ['Record', 'Rank_1', 'Team_1', 'Rank_2', 'Team_2', 'Rank_3', 'Team_3',
                      'USA', 'AP', 'DES', 'Mean', 'Median', 'St.Dev']

    drop_cols_2014 = ['Record', 'Rank_1', 'Team_1', 'Rank_2', 'Team_2', 'Rank_3', 'Team_3', 'D1A',
                      'USA', 'AP', 'DES', 'Mean', 'Median', 'St.Dev']

    drop_cols_2013 = ['Record', 'Rank_1', 'Team_1', 'Rank_2', 'Team_2', 'Rank_3', 'Team_3', 'D1A',
                      'USA', 'AP', 'DES', 'Mean', 'Median', 'St.Dev']

    drop_cols_2012 = ['Record', 'Rank_1', 'Team_1', 'Rank_2', 'Team_2', 'Rank_3', 'Team_3',
                      'USA', 'AP', 'DES', 'Mean', 'Median', 'St.Dev']

    drop_cols_2011 = ['Record', 'Rank_1', 'Team_1', 'Rank_2', 'Team_2',
                      'USA', 'AP', 'DES', 'Mean', 'Median', 'St.Dev']

    drop_cols_2010 = ['Record', 'Rank_1', 'Team_1', 'Rank_2', 'Team_2', 'TRX',
                      'USA', 'AP', 'DES', 'Mean', 'Median', 'St.Dev']

    drop_cols_2009 = ['Record', 'Rank_1', 'Team_1', 'Rank_2', 'Team_2', 'TRX',
                      'USA', 'AP', 'DES', 'Mean', 'Median', 'St.Dev']

    drop_cols_2008 = ['Record', 'Rank_1', 'Team_1', 'Rank_2', 'Team_2', 'LYN',
                      'USA', 'AP', 'DES', 'Mean', 'Median', 'St.Dev']

    drop_cols_2007 = ['Record', 'Rank_1', 'Team_1', 'Rank_2', 'Team_2', 'LYN',
                      'USA', 'AP', 'Mean', 'Median', 'St.Dev']

    drop_cols_2006 = ['Record', 'Rank_1', 'Team_1', 'TRX', 'LYN',
                      'USA', 'AP', 'Mean', 'Median', 'St.Dev']

    drop_cols_2005 = ['Record', 'Rank_1', 'Team_1', 'LYN', 'DES',
                      'USA', 'AP', 'Mean', 'Median', 'St.Dev']

    drop_cols_2004 = ['Record', 'Rank_1', 'Team_1', 'LYN', 'DES',
                      'USA', 'AP', 'Mean', 'Median', 'St.Dev']

    drop_cols_2003 = ['Record', 'Rank_1', 'Team_1', 
                      'USA', 'AP', 'Mean', 'Median', 'St.Dev']

    df.drop(columns=drop_cols_2003, inplace=True)

    f_name = 'data/rankings_' + str(season) + '.csv'
    csv_file = Path(f_name)
    if csv_file.is_file():
        os.remove(csv_file)

    df.to_csv(csv_file, sep=',', index=False )
    return


if __name__ == "__main__":
    run_main()

