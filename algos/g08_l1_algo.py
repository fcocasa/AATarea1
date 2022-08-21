from algos.l1_algo import L1Algo
import numpy as np
from aux_functions import adjust_params, goal_distance
import time


class G08L1Algo(L1Algo):
    """
    This is your algorithm. You will have to implement everything here
    """

    def __init__(self, **kwargs):
        super().__init__()
        self.learning_rate = 0.1
        # 0 =we do not care if you lose but are close to goal, 1= we do care
        self.closeness_reward = 0.8
        self.discount_factor = 0.9
        self.learning_cooldown = 0.8

    def fit(self, model, experiences):  # we want to maximize the reward. (WIN FAST)
        """
        Fits the given model to the new experiences.
        This is your algorithm. You will have to implement everything here
        """
        all_params = model.params
        print('all_params')
        print(all_params)

        if experiences[-1]['reward'] != 0:  # el ultimo reward me indica si llegue a la meta
            print('----------Llegue!!!----------')
            v_train = experiences[-1]['reward']
            print('reward')
            print(experiences[-1]['reward'])
        else:
            print('----------perdi----------')
            [gx, gy] = goal_distance(experiences[-1]['observation']['image'],
                                     experiences[-1]['agent_pos'][0], experiences[-1]['agent_pos'][1])
            taxi = gx + gy  # [1, world_len*world_len]
            # nocion de cercania para la penalizacion, si no quedo lejos, no penalizo "tanto"
            v_train = -1 + self.closeness_reward/taxi

            print('v_train', v_train)

        same_pos = -1  # keeps track of the agent being stuck on same position
        last_pos = experiences[-1]['agent_pos']

        for i in range(len(experiences)-1, -1, -1):  # recorro el arreglo en sentido inverso
            v_actual = model.evaluate(
                experiences[i]['observation'], experiences[i]['agent_pos'], experiences[i]['agent_dir'])
            model.params = adjust_params(
                model.params, experiences[i], self.learning_rate, v_train-v_actual)

            if (last_pos[0] == experiences[i]['agent_pos'][0] and last_pos[1] == experiences[i]['agent_pos'][1]):
                same_pos += 1
            else:
                same_pos = 0

            last_pos = experiences[i]['agent_pos']

            v_train = model.evaluate(
                experiences[i]['observation'], experiences[i]['agent_pos'], experiences[i]['agent_dir'])

            # v_train = model.evaluate(experiences[i]['observation'], experiences[i]['agent_pos'], experiences[i]['agent_dir'])
            if (same_pos < 3):  # apply discount factor only if we are not stuck in a position
                v_train = v_train*self.discount_factor

        print('model.params')
        print(model.params)

        # I reduce learning rate only if I won (I've learnt something)
        if (experiences[-1]['reward'] > 0):
            self.learning_rate = self.learning_rate * self.learning_cooldown

        return model
