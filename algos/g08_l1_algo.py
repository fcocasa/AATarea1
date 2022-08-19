from algos.l1_algo import L1Algo
import numpy as np
from aux_functions import adjust_params, goal_distance


class G08L1Algo(L1Algo):
    """ 
    This is your algorithm. You will have to implement everything here
    """

    def __init__(self, **kwargs):
        super().__init__()

        # TODO: Add metaparameters if needed! experiment with learning rateeee
        self.learning_rate = 0.5

    def fit(self, model, experiences):  # we want to maximize the reward. (WIN FAST)
        """
        Fits the given model to the new experiences.
        This is your algorithm. You will have to implement everything here
        """
        all_params = model.params
        print('all_params')
        print(all_params)

        v_train = experiences[-1]['reward']
        if experiences[-1]['reward'] != 0: # el ultimo reward me indica si llegue a la meta
            print('----------Llegue!!!----------')
            v_train = experiences[-1]['reward']
            print('reward')
            print(experiences[-1]['reward'])
        else:
            print('----------perdi----------')
            [gx, gy] = goal_distance(experiences[-1]['observation']['image'], experiences[-1]['agent_pos'][0], experiences[-1]['agent_pos'][1])
            taxi = gx + gy
            v_train = -1 + 0.5/taxi #nocion de cercania para la penalizacion, si no quedo lejos, no penalizo "tanto"


        for i in range(len(experiences)-1,-1,-1): #recorro el arreglo en sentido inverso
            v_actual = model.evaluate(experiences[i]['observation'],experiences[i]['agent_pos'],experiences[i]['agent_dir'])
            model.params = adjust_params(model.params,experiences[i],self.learning_rate,v_train-v_actual)
            #v_train = model.evaluate(experiences[i]['observation'],experiences[i]['agent_pos'],experiences[i]['agent_dir'])*0.5
            v_train = v_train*0.9
        print('model.params')
        print(model.params)

        self.learning_rate = self.learning_rate*0.9

        return model
