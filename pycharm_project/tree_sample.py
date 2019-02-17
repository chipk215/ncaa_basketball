
from anytree import Node, RenderTree
import random
import tournament_bracket


def predict_winner(t1, t2):
    random_choice = random.randint(1, 2)
    # print('random choice= ', random_choice)
    if random_choice % 2 == 0:
        return t1.team, t1.team_id
    else:
        return t2.team, t2.team_id


def build_bracket():

    bracket = tournament_bracket.TournamentBracket()
    print('East Section ---------')
    bracket.display_east_section()

    print('\nMidwest Section ---------')
    bracket.display_midwest_section()

    print('\nSouth Section---------')
    bracket.display_south_section()

    print('\nWest Section ---------')
    bracket.display_west_section()

    win_team, win_team_id = bracket.eval_east_section(predict_winner)
    print('\n\nEast Section ---------')
    bracket.display_east_section()

    print("East Winner= ", win_team)

    # print('---------')
    # for pre, _, node in RenderTree(root_node):
    #    print("%s%s" % (pre, node.team))


if __name__ == "__main__":
    build_bracket()
