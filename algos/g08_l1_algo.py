from algos.l1_algo import L1Algo
import numpy as np
from aux_functions import adjust_params


class G08L1Algo(L1Algo):
    """ 
    This is your algorithm. You will have to implement everything here
    """

    def __init__(self, **kwargs):
        super().__init__()

        # TODO: Add metaparameters if needed! experiment with learning rateeee
        self.learning_rate = 0.1

    def fit(self, model, experiences):  # we want to maximize the reward. (WIN FAST)
        """
        Fits the given model to the new experiences.
        This is your algorithm. You will have to implement everything here
        """
       # last_experience = {
        #     'observation': observation,
        #     'agent_pos': self.environment.agent_pos,
        #     'agent_dir': self.environment.agent_dir,
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
        # print('model--', model.gx_param)

        # model.update(new_gx, new_gy, new_f, new_r, new_b, new_l)

        """w_gf = model.gf_param
        w_gr = model.gr_param
        w_gb = model.gb_param
        w_gl = model.gl_param
        w_f = model.f_param
        w_r = model.r_param
        w_b = model.b_param
        w_l = model.l_param
        w_it = model.independent_term"""

        """w_e = model.e_param
        w_s = model.s_param
        w_w = model.w_param
        w_n = model.n_param
        w_it = model.independent_term"""


        """print(model.gx_param)
        print(model.gy_param)"""
        """print(model.gf_param)
        print(model.gr_param)
        print(model.gb_param)
        print(model.gl_param)
        print(model.f_param)
        print(model.r_param)
        print(model.b_param)
        print(model.l_param)
        print(model.independent_term)"""
        """print(model.e_param)
        print(model.s_param)
        print(model.w_param)
        print(model.n_param)"""

        #all_params = [w_gx,w_gy,w_e,w_s,w_w,w_n,w_it]
        #all_params = [w_gf,w_gr,w_gb,w_gl,w_f,w_r,w_b,w_l,w_it]

        all_params = model.params
        print('all_params')
        print(all_params)

        v_train = -1 + 2*experiences[-1]['reward']
        if experiences[-1]['reward'] != 0: # el ultimo reward me indica si llegue a la meta
            print('----------Llegue!!!----------')
        else:
            print('----------perdi----------')
        for i in range(len(experiences)-1,-1,-1): #recorro el arreglo en sentido inverso
            v_actual = model.evaluate(experiences[i]['observation'],experiences[i]['agent_pos'],experiences[i]['agent_dir'])
            model.params = adjust_params(model.params,experiences[i],self.learning_rate,v_train-v_actual)
            #v_train = model.evaluate(experiences[i]['observation'],experiences[i]['agent_pos'],experiences[i]['agent_dir'])*0.5
            v_train = v_train*0.9
        print('model.params')
        print(model.params)

        self.learning_rate = self.learning_rate*0.9

        return model
