"""
Quoridor ai example based on minimax tree search + alpha_beta prunning.
"""

from collections import deque
from math import sqrt

import numpy as np

from fights.base import BaseAgent
from fights.envs import quoridor

from minimax_helper import _agent_dis_to_end


class MinimaxAgent(BaseAgent):
    env_id = ("quoridor", 0)  # type: ignore

    def __init__(self, agent_id: int, seed: int = 0) -> None:
        self.agent_id = agent_id  # type: ignore
        self._rng = np.random.default_rng(seed)
        # self.depth = (3, 5, 8)
        self.depth = (2, 3, 4)

    def _possible_actions(self, state: quoridor.QuoridorState, agent_id: int):
        actions = quoridor.QuoridorEnv().legal_actions(state, agent_id)
        actions = np.nonzero(actions)
        actions = list(zip(actions[0], actions[1], actions[2]))
        return actions

    def _evaluation(self, state: quoridor.QuoridorState):
        mine, opps = _agent_dis_to_end(
            state.board, self.agent_id, quoridor.QuoridorEnv().board_size
        ), _agent_dis_to_end(state.board, 1 - self.agent_id, quoridor.QuoridorEnv().board_size)
        return (
            int(sqrt(opps * 15000))
            - int(sqrt(mine * 10000))
            + (
                state.walls_remaining[self.agent_id]
                - state.walls_remaining[1 - self.agent_id]
            )
            * 10
        )

    def __call__(self, state: quoridor.QuoridorState) -> quoridor.QuoridorAction:

        def search(
            state: quoridor.QuoridorState,
            agent_id: int,
            depth: int,
            lower_bound: int,
            upper_bound: int,
        ):
            if state.done:
                if agent_id == self.agent_id:
                    return -100000000
                else:
                    return 100000000
            if depth <= 0:
                return self._evaluation(state)

            new_agent_id = 1 - agent_id
            new_depth = depth - 1

            if agent_id == self.agent_id:
                best_score = -100000000
            else:
                best_score = 100000000

            actions = self._possible_actions(state, agent_id)
            for action in actions:
                new_state = quoridor.QuoridorEnv().step(state, agent_id, action)
                if agent_id == self.agent_id:
                    score = search(
                        new_state, new_agent_id, new_depth, best_score, upper_bound
                    )
                    if best_score < score:
                        best_score = score
                        if best_score > upper_bound:
                            break
                else:
                    score = search(
                        new_state, new_agent_id, new_depth, best_score, upper_bound
                    )
                    if best_score > score:
                        best_score = score
                        if best_score < lower_bound:
                            break
            return best_score

        if state.walls_remaining[0] > 0 and state.walls_remaining[1] > 0:
            searching_depth = self.depth[0]
        elif state.walls_remaining[0] == 0 and state.walls_remaining[1] == 0:
            searching_depth = self.depth[2]
        else:
            searching_depth = self.depth[1]

        max_score = -100000001
        score_lst = []
        best_actions = []
        actions = self._possible_actions(state, self.agent_id)
        for action in actions:
            new_state = quoridor.QuoridorEnv().step(state, self.agent_id, action)
            score = search(
                new_state, 1 - self.agent_id, searching_depth - 1, max_score, 100000001
            )
            score_lst.append(score)
            if score == max_score:
                best_actions.append(action)
            elif score > max_score:
                best_actions = [action]
                max_score = score

        return self._rng.choice(best_actions)
