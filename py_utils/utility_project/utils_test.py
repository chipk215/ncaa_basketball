import utils
import numpy as np


def check_value(expected_value, value):
    epsilon = 1E-6
    if abs(expected_value - value) < epsilon:
        return True
    else:
        return False


def log_loss_different_size_params_test():
    p1 = np.ones(10)
    p2 = np.ones(5)
    log_loss = utils.compute_log_loss(p1, p2)
    assert log_loss == -1
    print("Pass log_loss_different_size_params_test")


def simple_two_correct_prediction_test():
    expected_value = 0.1642520
    game_results = np.array([1, 1])
    probs = np.array([0.8, 0.9])
    result = utils.compute_log_loss(game_results, probs)
    check_result = check_value(expected_value, result)
    assert check_result == True
    print("Pass simple_two_correct_prediction_test")


def two_game_certain_wrong_test():
    expected_value = 6.907755778968009
    # t1 wins game 1, t2 wins game 2
    game_results = np.array([1, 0])

    # 100% certain t1 wins game 1, 100% certain t1 wins game 2 (big miss in game 2)
    probs = np.array([1.0, 1.0])
    result = utils.compute_log_loss(game_results, probs)
    check_result = check_value(expected_value, result)
    assert check_result == True
    print("Pass two_game_certain_wrong_test")


def tournament_test():
    game_results = np.array([1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1,
                             0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0,
                             1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1,
                             0, 1, 0, 1])

    probs = np.array([0.86888558, 0.3292557, 0.88046764, 0.30718927, 0.03538449,
                      0.08127584, 0.96943025, 0.6226326, 0.82244985, 0.38363198,
                      0.71069899, 0.43470625, 0.9713061, 0.02227577, 0.93232913,
                      0.08480705, 0.91622564, 0.39050279, 0.54235229, 0.26903521,
                      0.99601471, 0.0102425, 0.96365815, 0.68893848, 0.95450932,
                      0.29954549, 0.64884756, 0.57827661, 0.98739581, 0.01016094,
                      0.96647785, 0.1229016, 0.8410822, 0.51720818, 0.54511669,
                      0.32537434, 0.6954423, 0.49633855, 0.33026077, 0.18860028,
                      0.43493407, 0.81725354, 0.82162818, 0.67656312, 0.99026493,
                      0.22145372, 0.61613838, 0.07631663, 0.88026869, 0.09254519,
                      0.18685004, 0.4028804, 0.33188224, 0.54729476, 0.64012994,
                      0.21132237, 0.9297075, 0.75630015, 0.83546021, 0.07202357,
                      0.60908267, 0.30864824, 0.95217287, 0.54962558, 0.76507719,
                      0.13549928, 0.93355817])

    result = utils.compute_log_loss(game_results, probs)

    print(result)


def run_main():
    # log_loss_different_size_params_test()
    # simple_two_correct_prediction_test()
    # two_game_certain_wrong_test()
    tournament_test()


if __name__ == "__main__":
    run_main()

