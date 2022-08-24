import json
from models.l1_model import L1Model
from aux_functions import goal_step_distance, walls_distance, move_forward, walls_axis, goal_distance_orientation, try_forward
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
        self.last_action_forward = 0
        self.load()

    def action(self, observation, environment, visibility):
        # print('observation', observation)
        """
        Selects and action to perform given the state of the world.
        """

        agent_current_pos = environment.agent_pos  # x,y
        agent_current_dir = environment.agent_dir  # 0 f, 1 r, 2 b, 3 l
        value_left = self.evaluate(
            observation, agent_current_pos, (agent_current_dir-1) % 4, visibility)

        value_right = self.evaluate(
            observation, agent_current_pos, (agent_current_dir+1) % 4, visibility)

        new_agent_pos = try_forward(
            observation['image'], agent_current_pos, agent_current_dir)

        value_forward = self.evaluate(
            observation, new_agent_pos, agent_current_dir, visibility)

        if value_forward == max(value_left, value_right, value_forward):
            self.last_action_forward = 0
            return self.environment.actions.forward
        elif value_right == max(value_left, value_right, value_forward):
            self.last_action_forward += 1
            return self.environment.actions.right
        else:
            self.last_action_forward += 1
            return self.environment.actions.left

    def evaluate(self, observation, agent_pos, agent_dir, visibility):
        """
        Evaluates the given observation and returns its value.
        """
        [gx, gy] = goal_step_distance(observation['image'],
                                      agent_pos[0], agent_pos[1], agent_dir, visibility)
        [f, r, b, l] = walls_distance(
            observation['image'], agent_pos[0], agent_pos[1], agent_dir, visibility)
            
        values = [gx, gy, f, r, l, 1]

        value = 0
        for i in range(len(values)):
            value += values[i]*self.params[i]

        return value

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

        model_config = {
            'params': self.params
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
        return f"Parameters Gx:{self.params[0]} Gy:{self.params[1]} F:{self.params[2]} R:{self.params[3]} B:{self.params[4]} L:{self.params[5]} Indep:{self.params[6]} "
