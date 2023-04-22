"""
Puoribor game example.
Prints board state to stdout with random agents by default.
Run `python puoribor.py -h` for more information.
"""

import re
import sys
import colorama
from colorama import Fore, Style
from fights.envs import quoridor
from minimax_agent import MinimaxAgent

sys.path.append("../")


def fallback_to_ascii(s: str) -> str:
    try:
        s.encode(sys.stdout.encoding)
    except UnicodeEncodeError:
        s = re.sub("[┌┬┐├┼┤└┴┘╋]", "+", re.sub("[─━]", "-", re.sub("[│┃]", "|", s)))
    return s


def colorize_walls(s: str) -> str:
    return s.replace("━", Fore.BLUE + "━" + Style.RESET_ALL).replace(
        "┃", Fore.RED + "┃" + Style.RESET_ALL
    )


def run():
    assert quoridor.QuoridorEnv.env_id == MinimaxAgent.env_id
    colorama.init()

    state = quoridor.QuoridorEnv().initialize_state()
    agents = [MinimaxAgent(0), MinimaxAgent(1)]

    iter_num = 0
    while not state.done:
        print(fallback_to_ascii(colorize_walls(str(state))))
        for agent in agents:
            action = agent(state)
            state = quoridor.QuoridorEnv().step(state, agent.agent_id, action)
            print(fallback_to_ascii(colorize_walls(str(state))))
            # a = input()
            if state.done:
                print(f"agent {agent.agent_id} won in {iter_num} iters")
                break
        iter_num += 1
    return


if __name__ == "__main__":
    run()
