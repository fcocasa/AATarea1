import json
from models.l1_model import L1Model
from aux_functions import goal_distance, walls_distance, try_forward, walls_axis, goal_distance_orientation
from gym_minigrid import wrappers
import numpy as np
import random

class G08L1Model(L1Model):
    """
    This is a dummy implementation of the model:

        - It has two modes of selecting actions: (1) randomly or (2) from a pre-defined sequence of actions. 
        This can be set with the 'cheat_mode' and 'cheat_movs' parameters.
        - It does not learn, since updates does nothing
        - In fact it doesn't store anything regarding its status but a variable "my_param"... so it's as dummy as you can get.
        - stores the model as a json (instead of pickling)

    Feel free to change ALL of it.
    """

    def __init__(self, environment, **kwargs):
        super().__init__(environment)

        # Values to load/store the model
        self.name = kwargs.get('name', 'my_model')
        self.file_path = kwargs.get('file_path', './trained_models/')

        # Parameters of the model TODO: check gx and gy should be bigger to step out max_mov value in Hypotesis space

        self.load()

        

    def action(self, observation, environment, type):# type es pra hacer mov random
        """
        Selects and action to perform given the state of the world.
        """
        if type == 0:
            agent_current_pos = environment.agent_pos
            agent_current_dir = environment.agent_dir
            # 0 f, 1 r, 2 b, 3 l
            value_left = self.evaluate(observation, agent_current_pos, (agent_current_dir-1)%4)
            
            value_right = self.evaluate(observation, agent_current_pos, (agent_current_dir+1)%4)
            
            new_agent_pos = try_forward(observation['image'],agent_current_pos,agent_current_dir)
            # print('new_agent_pos')
            # print(new_agent_pos)
            # print('agent_pos')
            # print(agent_current_pos)
            if new_agent_pos[0] != agent_current_pos[0] or new_agent_pos[1] != agent_current_pos[1] :
                value_forward = self.evaluate(observation, new_agent_pos, agent_current_dir)
            else:
                value_forward=min(value_left,value_right)

            if value_left == max(value_left,value_right,value_forward):
                print('left')
                return self.environment.actions.left
            elif value_right == max(value_left,value_right,value_forward):
                print('right')
                return self.environment.actions.right
            else:
                print('forward')
                return self.environment.actions.forward

            # if value_forward == max(value_left,value_right,value_forward):
            #     print('foward')
            #     return self.environment.actions.forward
            # else:
            #     print('right or left')
            #     moves = [self.environment.actions.left,self.environment.actions.right]
            #     return random.choice(moves)
        else:#type random move
            moves = [self.environment.actions.left,self.environment.actions.right,self.environment.actions.forward]
            return random.choice(moves)


    def evaluate(self, observation, agent_pos, agent_dir):#evaluate(self, observation, environment):
        """
        Evaluates the given observation and returns its value.
        """
        [gx, gy] = goal_distance(observation['image'], agent_pos[0], agent_pos[1])
        [f, r, b, l] = walls_distance(observation['image'], agent_pos[0], agent_pos[1], agent_dir)

        # [gx, gy, gf, gr, gb, gl] = goal_distance_orientation(observation['image'], agent_pos[0], agent_pos[1], agent_dir)

        #values = [gf,gr,gb,gl,f,r,l,b,1]
        values = [gx,gy,f,r,b,l,1]
        
        value = 0
        for i in range(6):
            value += values[i]*self.params[i]

        return value

        #return gf*self.gf_param+ gb*self.gb_param+gl*self.gl_param + gl*self.gl_param + e*self.e_param + s*self.s_param + w*self.w_param + n*self.n_param + self.independent_term
        #return gx*self.gx_param + gy*self.gy_param + f*self.f_param + b*self.b_param + l*self.l_param + r*self.r_param + self.independent_term
        #return gf*self.gf_param+ gb*self.gb_param+gl*self.gl_param + gl*self.gl_param + f*self.f_param + b*self.b_param + l*self.l_param + r*self.r_param + self.independent_term

    def load(self):
        """
        Loads the model as json to the configured dir/file_name
        """
        file_name = f"{self.file_path}{self.name}.json"
        with open(file_name, 'r') as openfile:
            json_config = json.load(openfile)
            self.params = json_config['params']

    def save(self):
        """
        Saves the model as json to the configured dir/file_name
        """

        # TODO: adapt this to your solution!
        model_config = {
            'params':self.params
        }
        json_config = json.dumps(model_config, indent=2)

        file_name = f"{self.file_path}{self.name}.json"
        with open(file_name, "w") as outfile:
            outfile.write(json_config)

    def update(parameters, **params):
        for i in range(len(parameters)):
            self.params[i] = parameters[i]
        return self

    def __str__(self):
        return f"Parameters Gx:{self.gx_param} Gy:{self.gy_param} F:{self.f_param} R:{self.r_param} B:{self.b_param} L:{self.l_param} "
