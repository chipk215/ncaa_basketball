from bs4 import BeautifulSoup
import requests


def make_csv_line(line):
    no_comma = line.lstrip(' ').replace(',', '')
    words = no_comma.split()
    stripped_words = []
    for word in words:
        stripped_words.append(word.strip())
    return ','.join(stripped_words)


def run_main():

    source = requests.get('https://www.masseyratings.com/cb/arch/compare2018-18.htm').text
    soup = BeautifulSoup(source, 'lxml')
    pre = soup.find('pre')

    start_section_text = 'WLK BWE'
    end_section_text = '--------------------'

    page_text = pre.text.strip()
    start_position = page_text.find(start_section_text)
    end_position = page_text.find(end_section_text)

    table_text = page_text[start_position:end_position]

    lines = table_text.splitlines()

    first_column_copied = False
    result = []
    for line in lines:
        # handle blank lines
        if not line:
            # blank line do not copy into result
            continue
        elif line.lstrip(' ').startswith(start_section_text):
            if not first_column_copied:
                result.append(make_csv_line(line))
                first_column_copied = True
            else:
                continue
        else:
            # not a blank line or a column header
            result.append(make_csv_line(line))

    print(len(result))
    return


if __name__ == "__main__":
    run_main()

