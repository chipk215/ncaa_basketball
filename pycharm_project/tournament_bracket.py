import pandas as pd
from pathlib import Path
from anytree import Node, RenderTree


class TournamentBracket:

    def build_bracket(self, section):
        nodes = []

        # leaf nodes
        for i in range(16):
            label = 'l_16_' + str(i)
            seed_value = self.index_to_seed[i]
            team_name = section.loc[section.seed == seed_value, 'team'].to_list()[0]
            team_id = section.loc[section.seed == seed_value, 'id'].to_list()[0]
            nodes.append(Node(label, team=team_name, team_id=team_id))

        # 2nd level of 8 nodes
        child_index = 0
        for i in range(16, 24):
            node = Node('l_8_' + str(i - 15), team='', team_id='')
            node.children = [nodes[child_index], nodes[child_index + 1]]
            nodes.append(node)
            child_index += 2

        # 3rd level of 4 nodes
        child_index = 16
        for i in range(24, 28):
            node = Node('l_4_' + str(i - 23), team='', team_id='')
            node.children = [nodes[child_index], nodes[child_index + 1]]
            nodes.append(node)
            child_index += 2

        # 4th level of 2 nodes
        child_index = 24
        for i in range(28, 30):
            node = Node('l_2_' + str(i - 27), team='', team_id='')
            node.children = [nodes[child_index], nodes[child_index + 1]]
            nodes.append(node)
            child_index += 2

        root_node = Node('ROOT', team='', team_id='')
        root_node.children = [nodes[28], nodes[29]]
        nodes.append(root_node)
        return nodes

    def __init__(self):

        self.index_to_seed = {0: 1, 1: 16, 2: 8, 3: 9, 4: 5, 5: 12, 6: 4, 7: 13, 8: 6, 9: 11,
                              10: 3, 11: 14, 12: 7, 13: 10, 14: 2, 15: 15}

        # Read file with tournament teams
        teams_file = "data/teams_2019.csv"
        self.tournament_teams = pd.read_csv(Path(teams_file))

        self.east_section = self.tournament_teams[self.tournament_teams['quadrant'] == 'East']
        self.east_nodes = self.build_bracket(self.east_section)

        self.midwest_section = self.tournament_teams[self.tournament_teams['quadrant'] == 'Midwest']
        self.midwest_nodes = self.build_bracket(self.midwest_section)

        self.south_section = self.tournament_teams[self.tournament_teams['quadrant'] == 'South']
        self.south_nodes = self.build_bracket(self.south_section)

        self.west_section = self.tournament_teams[self.tournament_teams['quadrant'] == 'West']
        self.west_nodes = self.build_bracket(self.west_section)

        return

    def display_east_section(self):
        for pre, _, node in RenderTree(self.east_nodes[30]):
            print("%s%s" % (pre, node.team))
        return

    def display_midwest_section(self):
        for pre, _, node in RenderTree(self.midwest_nodes[30]):
            print("%s%s" % (pre, node.team))
        return

    def display_south_section(self):
        for pre, _, node in RenderTree(self.south_nodes[30]):
            print("%s%s" % (pre, node.team))
        return

    def display_west_section(self):
        for pre, _, node in RenderTree(self.west_nodes[30]):
            print("%s%s" % (pre, node.team))
        return

    def tree_eval(self, node, eval_func):

        if not node.is_leaf:
            children = list(node.children)

            t1 = self.tree_eval(children[0], eval_func)
            t2 = self.tree_eval(children[1], eval_func)
            team, team_id = eval_func(t1, t2)
            node.team = team
            node.team_id = team_id
        return node

    def eval_east_section(self, eval_func):
        result = self.tree_eval(self.east_nodes[30], eval_func)
        return result.team, result.team_id
