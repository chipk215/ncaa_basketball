import pandas as pd
from pathlib import Path
from anytree import Node, RenderTree
import random


def predict_winner(t1, t2):
    random_choice = random.randint(1, 2)
    # print('random choice= ', random_choice)
    if random_choice % 2 == 0:
        return t1
    else:
        return t2


def tree_eval(node):

    if not node.is_leaf:
        children = list(node.children)

        t1 = tree_eval(children[0])
        t2 = tree_eval(children[1])
        winner = predict_winner(t1, t2)
        node.team = winner.team

    return node


def run_main():
    random.seed(215)
    node_16_1 = Node('level_16_1', team='')

    node_32_1 = Node('level_32_1', team='', parent=node_16_1)

    node_64_1 = Node('level_64_1', team='Duke', parent=node_32_1)
    node_64_16 = Node('level_64_16', team='Bucknell', parent=node_32_1)

    node_32_2 = Node('level_32_2', team='', parent=node_16_1)
    node_64_8 = Node('level_64_8', team='Washington', parent=node_32_2)
    node_64_9 = Node('level_64_16', team='Ohio State', parent=node_32_2)
    print(RenderTree(node_16_1))

    winner = tree_eval(node_16_1)
    print(winner.team)

    print(node_16_1.team)

    print(RenderTree(node_16_1))


index_to_seed = {
    0: 1,
    1: 16,
    2: 8,
    3: 9,
    4: 5,
    5: 12,
    6: 4,
    7: 13,
    8: 6,
    9: 11,
    10: 3,
    11: 14,
    12: 7,
    13: 10,
    14: 2,
    15: 15
}


def build_bracket():
    teams_file = "data/teams_2019.csv"
    tournament_teams = pd.read_csv(Path(teams_file))
    # print(tournament_teams)
    print(tournament_teams.shape)

    east_section = tournament_teams[tournament_teams['quadrant'] == 'East']
    nodes = []

    # leaf nodes
    for i in range(16):
        label = 'l_16_' + str(i)
        seed_value = index_to_seed[i]
        team_name = east_section.loc[east_section.seed == seed_value, 'team'].to_list()[0]
        nodes.append(Node(label, team=team_name))

    # 2nd level of 8 nodes
    child_index = 0
    for i in range(16, 24):
        node = Node('l_8_' + str(i-15), team='')
        node.children = [nodes[child_index], nodes[child_index+1]]
        nodes.append(node)
        child_index += 2

    # 3rd level of 4 nodes
    child_index = 16
    for i in range(24, 28):
        node = Node('l_4_' + str(i-23), team='')
        node.children = [nodes[child_index], nodes[child_index+1]]
        nodes.append(node)
        child_index += 2

    # 4th level of 2 nodes
    child_index = 24
    for i in range(28, 30):
        node = Node('l_2_' + str(i-27), team='')
        node.children = [nodes[child_index], nodes[child_index+1]]
        nodes.append(node)
        child_index += 2

    root_node = Node('ROOT', team='')
    root_node.children = [nodes[28], nodes[29]]
    nodes.append(root_node)

    for pre, _, node in RenderTree(root_node):
        print("%s%s" % (pre, node.team))

    tree_eval(root_node)

    print('---------')
    for pre, _, node in RenderTree(root_node):
        print("%s%s" % (pre, node.team))


if __name__ == "__main__":
    # run_main()
    build_bracket()
