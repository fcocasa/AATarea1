import json
from models.l1_model import L1Model


class GXL1Model(L1Model):
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

        # Parameters of the model
        # TODO: change this!
        self.my_parm = 0

        # Let's check if cheat mode is on!
        self.cheat_mode = kwargs.get('cheat_mode', False)
        if self.cheat_mode:
            self.cheat_mov = 0
            # Load the sequence of cheat moves, or use F,F,R,F,F by default
            self.cheat_movs = kwargs.get('cheat_movs', [
                self.environment.actions.forward,
                self.environment.actions.forward,
                self.environment.actions.right,
                self.environment.actions.forward,
                self.environment.actions.forward
            ])


    def action(self, observation):
        """
        Selects and action to perform given the state of the world.
        This dummy agent will select one action randomly, or, if active, an action
        from its list of cheat actions.
        """         
        # TODO: change this dummy code!
        if self.cheat_mode:
            # cycle the list of cheat movs
            next_action = self.cheat_movs[self.cheat_mov]
            self.cheat_mov = (self.cheat_mov + 1) % len(self.cheat_movs)
        else:
            # Pick a random action
            next_action = self.environment.action_space.sample()

        return next_action


    def evaluate(self, observation):
        """
        Evaluates the given observation and returns its value.
        """
        # TODO: change this dummy code!
        obs_value = self.my_parm * 5

        return obs_value


    def load(self):
        """
        Loads the model as json to the configured dir/file_name
        """                
        file_name = f"{self.file_path}{self.name}.json" 
        with open(file_name, 'r') as openfile:
            json_config = json.load(openfile)

        # TODO: adapt this to your solution!
        self.my_parm = json_config['my_parm']
        

    def save(self):
        """
        Saves the model as json to the configured dir/file_name
        """     

        # TODO: adapt this to your solution!
        model_config = {
            'my_parm': self.my_parm
        }
        json_config = json.dumps(model_config, indent=2)

        file_name = f"{self.file_path}{self.name}.json" 
        with open(file_name, "w") as outfile:
            outfile.write(json_config)


    def update(self, **params):
        """
        Updates the model with the given parameters
        """        
        # TODO: adapt this to your solution!

        return self


        