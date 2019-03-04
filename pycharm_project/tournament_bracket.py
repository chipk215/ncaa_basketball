import pandas as pd
from pathlib import Path
from anytree import Node, RenderTree
import sys
if sys.path[0] != '../py_utils':
    sys.path.insert(0,'../py_utils')

import py_utils.utils as utils

def get_team_record(summary_data_with_rankings, team_id, seed, is_opposition):
    team = summary_data_with_rankings[summary_data_with_rankings['team_id'] == team_id].copy()
    team['seed'] = seed
    if is_opposition:
        team = team.rename(columns={'season': 'season_o', 'school': 'school_o', 'team_id': 'team_id_o', 'srs': 'srs_o',
                                    'sos': 'sos_o', 'win_pct': 'win_pct_o', 'pts_avg': 'pts_avg_o',
                                    'opp_pts_avg': 'opp_pts_avg_o', 'fg_pct': 'fg_pct_o', 'ft_pct': 'ft_pct_o',
                                    'poss_avg': 'poss_avg_o', 'off_rebs_avg': 'off_rebs_avg_o',
                                    'def_rebs_avg': 'def_rebs_avg_o',
                                    'to_avg': 'to_avg_o', 'steal_avg': 'steal_avg_o', 'off_rating': 'off_rating_o',
                                    'ft_att_avg': 'ft_att_avg_o', 'SAG': 'sag_o', 'WLK': 'wlk_o', 'WOL': 'wol_o',
                                    'RTH': 'rth_o', 'COL': 'col_o', 'POM': 'pom_o', 'DOL': 'dol_o', 'MOR': 'mor_o',
                                    'seed': 'seed_o'})
    else:
        team = team.rename(columns={'season': 'season_t', 'school': 'school_t', 'team_id': 'team_id_t', 'srs': 'srs_t',
                                    'sos': 'sos_t', 'win_pct': 'win_pct_t', 'pts_avg': 'pts_avg_t',
                                    'opp_pts_avg': 'opp_pts_avg_t',
                                    'fg_pct': 'fg_pct_t', 'ft_pct': 'ft_pct_t', 'poss_avg': 'poss_avg_t',
                                    'off_rebs_avg': 'off_rebs_avg_t', 'def_rebs_avg': 'def_rebs_avg_t',
                                    'to_avg': 'to_avg_t',
                                    'steal_avg': 'steal_avg_t', 'off_rating': 'off_rating_t',
                                    'ft_att_avg': 'ft_att_avg_t',
                                    'SAG': 'sag_t', 'WLK': 'wlk_t', 'WOL': 'wol_t', 'RTH': 'rth_t', 'COL': 'col_t',
                                    'POM': 'pom_t',
                                    'DOL': 'dol_t', 'MOR': 'mor_t', 'seed': 'seed_t'})

    team = team.reset_index(drop=True)

    return team


def compute_top_conference_values(team_conferences, top_tournament_conferences, delta_game_record):
    t1_id = delta_game_record.iloc[0]['team_id_t']
    t2_id = delta_game_record.iloc[0]['team_id_o']
    t1_conference = team_conferences[team_conferences['id']== t1_id]['conf_name'].values[0]
    t2_conference = team_conferences[team_conferences['id']== t2_id]['conf_name'].values[0]
    # if both teams in same conference return 0,0 - no advantage
    if t1_conference == t2_conference:
        return 0,0
    t1_top_conference = t1_conference in top_tournament_conferences
    t2_top_conference = t2_conference in top_tournament_conferences
    if t1_top_conference == t2_top_conference:
        # both teams in or out of a top conference
        return 0,0
    if t1_top_conference:
        return 1,0
    else:
        return 0,1


class TournamentBracket:

    def build_bracket(self, section):
        nodes = []

        # leaf nodes
        for i in range(16):
            label = 'l_16_' + str(i)
            seed_value = self.index_to_seed[i]
            teams = section.loc[section.seed == seed_value, 'team']

            team_name = teams.values.to_list()[0]
            team_id = section.loc[section.seed == seed_value, 'id'].values.to_list()[0]
            nodes.append(Node(label, team=team_name, team_id=team_id, seed=seed_value))

        # 2nd level of 8 nodes
        child_index = 0
        for i in range(16, 24):
            node = Node('l_8_' + str(i - 15), team='', team_id='', seed='')
            node.children = [nodes[child_index], nodes[child_index + 1]]
            nodes.append(node)
            child_index += 2

        # 3rd level of 4 nodes
        child_index = 16
        for i in range(24, 28):
            node = Node('l_4_' + str(i - 23), team='', team_id='', seed='')
            node.children = [nodes[child_index], nodes[child_index + 1]]
            nodes.append(node)
            child_index += 2

        # 4th level of 2 nodes
        child_index = 24
        for i in range(28, 30):
            node = Node('l_2_' + str(i - 27), team='', team_id='', seed='')
            node.children = [nodes[child_index], nodes[child_index + 1]]
            nodes.append(node)
            child_index += 2

        root_node = Node('ROOT', team='', team_id='', seed='')
        root_node.children = [nodes[28], nodes[29]]
        nodes.append(root_node)
        return nodes

    def __init__(self):

        self.index_to_seed = {0: 1, 1: 16, 2: 8, 3: 9, 4: 5, 5: 12, 6: 4, 7: 13, 8: 6, 9: 11,
                              10: 3, 11: 14, 12: 7, 13: 10, 14: 2, 15: 15}

        # Read file with tournament teams
        teams_file = "../Data/teams_2019.csv"
        self.tournament_teams = pd.read_csv(Path(teams_file))

        self.east_section = self.tournament_teams[self.tournament_teams['quadrant'] == 'East']
        self.east_nodes = self.build_bracket(self.east_section)

        self.midwest_section = self.tournament_teams[self.tournament_teams['quadrant'] == 'Midwest']
        self.midwest_nodes = self.build_bracket(self.midwest_section)

        self.south_section = self.tournament_teams[self.tournament_teams['quadrant'] == 'South']
        self.south_nodes = self.build_bracket(self.south_section)

        self.west_section = self.tournament_teams[self.tournament_teams['quadrant'] == 'West']
        self.west_nodes = self.build_bracket(self.west_section)

        self.west_winner = None
        self.midwest_winner = None
        self.east_winner = None
        self.south_winner = None

        return

    def set_team_conferences(self, team_conferences):
        self.team_conferences = team_conferences

    def set_top_tournament_conferences(self, top_tournament_conferences):
        self.top_tournament_conferences = top_tournament_conferences

    def set_model_features(self, model_features):
        self.model_features = model_features

    def set_numeric_features(self, numeric_features):
        self.numeric_features = numeric_features

    def set_scaler(self, scaler):
        self.scaler = scaler

    def set_classifier(self, classifier):
        self.classifier = classifier

    def set_summary_data(self, summary_data):
        self.summary_data = summary_data

    def predict_winning_team(self, t1, t2):
        team_t = get_team_record(self.summary_data, t1.team_id, t1.seed, False)
        team_opp = get_team_record(self.summary_data, t2.team_id, t2.seed, True)
        game_record_df = pd.concat([team_t, team_opp], axis=1, sort=False)
        delta_game_record = utils.compute_delta_features(game_record_df)

        t1_top, t2_top = compute_top_conference_values(self.team_conferences, self.top_tournament_conferences,
                                                       delta_game_record)

        delta_game_record['top_conf_t'] = t1_top
        delta_game_record['top_conf_o'] = t2_top

        prediction_record = delta_game_record[self.model_features].copy()

        for item in self.numeric_features:
            prediction_record[item] = prediction_record[item].astype(float)

        prediction_record[self.numeric_features] = self.scaler.transform(prediction_record[self.numeric_features])

        y_predict = self.classifier.predict(prediction_record)
        #  print("y_predict= ", y_predict[0])

        if y_predict[0] == 1:
            return t1.team, t1.team_id
        else:
            return t2.team, t2.team_id

    def display_east_section(self):
        for pre, _, node in RenderTree(self.east_nodes[30]):
            print("%s(%s) %s" % (pre, node.seed, node.team))
        return

    def display_midwest_section(self):
        for pre, _, node in RenderTree(self.midwest_nodes[30]):
            print("%s(%s) %s" % (pre, node.seed, node.team))
        return

    def display_south_section(self):
        for pre, _, node in RenderTree(self.south_nodes[30]):
            print("%s(%s) %s" % (pre, node.seed, node.team))
        return

    def display_west_section(self):
        for pre, _, node in RenderTree(self.west_nodes[30]):
            print("%s(%s) %s" % (pre, node.seed, node.team))
        return

    def build_final_four(self):
        self.s1_node = Node('semi_east_west', team='', team_id='', seed='')
        self.east_winner.parent = self.s1_node
        self.west_winner.parent = self.s1_node
        self.east_winner.children = []
        self.west_winner.children = []

        self.s2_node = Node('semi_south_midwest', team='', team_id='', seed='')
        self.south_winner.parent = self.s2_node
        self.midwest_winner.parent = self.s2_node
        self.south_winner.children = []
        self.midwest_winner.children = []

        self.winning_node = Node('tourney_winner', team='', team_id='', seed='')
        self.winning_node.children = [self.s1_node, self.s2_node]
        self.winning_node.parent = None

        self.display_final_four()
        return

    def display_final_four(self):
        for pre, _, node in RenderTree(self.winning_node):
            print("%s(%s) %s" % (pre, node.seed, node.team))
        return

    def tree_eval(self, node, debug=False):

        if debug:
            print('Node Team:', node.team)

        if not node.is_leaf:
            children = list(node.children)
            if debug:
                for child in children:
                    print(child)

            t1 = self.tree_eval(children[0])
            t2 = self.tree_eval(children[1])
            team, team_id = self.predict_winning_team(t1, t2)
            node.team = team
            node.team_id = team_id
            if team == t1.team:
                node.seed = t1.seed
            else:
                node.seed = t2.seed

        return node

    def eval_east_section(self):
        result = self.tree_eval(self.east_nodes[30])
        self.east_winner = result
        return result.team, result.team_id, result.seed

    def eval_west_section(self):
        result = self.tree_eval(self.west_nodes[30])
        self.west_winner = result
        return result.team, result.team_id, result.seed

    def eval_midwest_section(self):
        result = self.tree_eval(self.midwest_nodes[30])
        self.midwest_winner = result
        return result.team, result.team_id, result.seed

    def eval_south_section(self):
        result = self.tree_eval(self.south_nodes[30])
        self.south_winner = result
        return result.team, result.team_id, result.seed

    def eval_final_four(self):
        result = self.tree_eval(self.winning_node, True)
        return result.team, result.team_id, result.seed


def run_main():
    bracket = TournamentBracket()
    


if __name__ == "__main__":
    run_main()