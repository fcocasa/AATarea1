from algos.l1_algo import L1Algo
import numpy as np


class G08L1Algo(L1Algo):
    """ 
    This is your algorithm. You will have to implement everything here
    """

    def __init__(self, **kwargs):
        super().__init__()

        # TODO: Add metaparameters if needed! experiment with learning rateeee
        self.learning_rate = 0.001

    def fit(self, model, last_experience):  # we want to maximize the reward. (WIN FAST)
        """
        Fits the given model to the new experiences.
        This is your algorithm. You will have to implement everything here
        """
        # last_experience = {
        #     'observation': observation,
        #     'value': start_value,
        #     'action': action,
        #     'next_observation': next_observation,
        #     'next_value': reward if done else next_value,
        #     'done': done,
        #     'reward': reward
        # }

        # new_gx= gx + self.learning_rate ()
        # new_gy = gy + self.learning_rate()

        # new_f = f + self.learning_rate()
        # new_f =  + self.learning_rate()
        print('model--', model.gx_param)

        # model.update(new_gx, new_gy, new_f, new_r, new_b, new_l)

        return model
