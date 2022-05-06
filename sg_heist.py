#!/usr/bin/env python3
# PYTHON_ARGCOMPLETE_OK
"""
S&G Heist rb calculator
"""

import argparse
import random
import argcomplete


def _get_arg_parser():
    """
    Return arguments parser
    """

    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument("-f", "--first",
                        dest="first",
                        action="store",
                        type=float,
                        help="Probability of finishing first",
                        default=.333,
                        )
    parser.add_argument("-s", "--second",
                        dest="second",
                        action="store",
                        type=float,
                        help="Probability of finishing second",
                        default=.333,
                        )
    parser.add_argument("-n", "--simulations",
                        dest="n_simu",
                        action="store",
                        type=int,
                        default=5000,
                        help="Number of simulations",
                        )
    parser.add_argument("-V", "--verbose",
                        dest="verbose",
                        action="store_true",
                        default=False,
                        help="increase vebosity",
                        )
    return parser


def sg_position(probability_first, probability_second):
    """
    Return random position
    """
    rand = random.random()
    if rand < probability_first:
        return 1
    if rand < probability_first + probability_second:
        return 2
    return 3


def sg_heist_run(probability_first, probability_second):
    """
    Run a S&G heist challenge
    Return S&G positions
    """
    sg_samples = []
    while True:
        sg_samples.append(sg_position(probability_first, probability_second))
        if sg_samples.count(1) == 10:
            break
        if sg_samples.count(3) == 3:
            break
#     print(sg_samples)
    return sg_samples


def sg_heist_run_all(probability_first, probability_second):
    """
    Run all challenges
    Return number of games and number of bonuses
    """
    HEIST_ATTEMPTS=50
    games = []
    bonus = []
    for _ in range(HEIST_ATTEMPTS):
        sgs = sg_heist_run(probability_first, probability_second)
        games.append(len(sgs))
        bonus.append(sg_bonus(sgs))
    return games, bonus


def sg_bonus(samples):
    """
    Return number of bonus
    """
    if samples.count(1) == 10:
        return 32
    if samples.count(1) >= 8:
        return 12
    if samples.count(1) >= 6:
        return 4
    if samples.count(1) >= 4:
        return 1
    return 0


def main():
    """
    Main
    """
    parser = _get_arg_parser()
    argcomplete.autocomplete(parser)
    args = parser.parse_args()

    RAKE=.07
    simu_games = []
    simu_bonus = []
    for i in range(args.n_simu):
        games, bonus = sg_heist_run_all(args.first, args.second)
#         print("Run {}: {} games, bonus {}".format(j, len(sgs), sg_bonus(sgs)))
        simu_games.append(sum(games))
        simu_bonus.append(sum(bonus))
        if args.verbose:
            rakeback = sum(bonus) / (sum(games) *RAKE)
            print("Run {}: {} games, bonus {}, rb {}".format(i, simu_games[-1],
                                                             simu_bonus[-1], rakeback))
#         print("rb {}".format(rb))
    rakeback = sum(simu_bonus) / (sum(simu_games) * RAKE)
    print("rakeback {}".format(rakeback))
    print("{} games on average".format(sum(simu_games)/args.n_simu))
    print("{} bonuses on average".format(sum(simu_bonus)/args.n_simu))


if __name__ == '__main__':
    main()
