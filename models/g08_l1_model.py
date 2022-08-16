import json
from models.l1_model import L1Model
from gym_minigrid import wrappers

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

        # Parameters of the model
        self.gx_param = 0
        self.gy_param = 0
        self.f_param = 0
        self.r_param = 0
        self.l_param = 0
        self.b_param = 0

        # Let's check if cheat mode is on!
        # self.cheat_mode = kwargs.get('cheat_mode', False)
        # if self.cheat_mode:
        #     self.cheat_mov = 0
        #     # Load the sequence of cheat moves, or use F,F,R,F,F by default
        #     self.cheat_movs = kwargs.get('cheat_movs', [
        #         self.environment.actions.forward,
        #         self.environment.actions.forward,
        #         self.environment.actions.right,
        #         self.environment.actions.forward,
        #         self.environment.actions.forward
        #     ])

    def action(self, observation):
        """
        Selects and action to perform given the state of the world.
        """

        # Evaluate all possible movements and select greatest score
        # TODO: arreglar, falta entender como hacer un movimiento (o sea generar un environment) a partir de un observation
        right_action_score = self.evaluate(wrappers.SymbolicObsWrapper(environment_movderecha))
        left_action_score = self.evaluate(wrappers.SymbolicObsWrapper(environment_movizquierda))
        forward_action_score = self.evaluate(wrappers.SymbolicObsWrapper(environment_movadelante))
        if right_action_score > left_action_score and right_action_score > forward_action_score:
            next_action = self.environment.actions.right
        else:
            if left_action_score > forward_action_score:
                next_action = self.environment.actions.left
            else:
                next_action = self.environment.actions.forward

        return next_action

    def evaluate(self, observation):
        """
        Evaluates the given observation and returns its value.
        """
        # TODO: change this dummy code!  EVALUAR EL TABLERO Y RETORNAR COMBINACIÓN LINEAL USANDO LOS PARAMETROS DEL MODELO
        obs_value = 5

        return obs_value

    def load(self):
        """
        Loads the model as json to the configured dir/file_name
        """
        file_name = f"{self.file_path}{self.name}.json"
        with open(file_name, 'r') as openfile:
            json_config = json.load(openfile)

        # TODO: adapt this to your solution!
        self.gx_param = json_config['gx_param']

    def save(self):
        """
        Saves the model as json to the configured dir/file_name
        """

        # TODO: adapt this to your solution!
        model_config = {
            'gx_param': self.gx_param
        }
        json_config = json.dumps(model_config, indent=2)

        file_name = f"{self.file_path}{self.name}.json"
        with open(file_name, "w") as outfile:
            outfile.write(json_config)

    def update(self, gx, gy, f, r, l, b, **params):
        self.gx = gx
        self.gy = gy
        self.f = f
        self.r = r
        self.l = l
        self.b = b
        return self
        """
        Updates the model with the given parameters
        """
        # TODO: adapt this to your solution!

        return self

    def __str__(self):
        return f"Parameters Gx:{self.gx_param} Gy:{self.gy_param} F:{self.f_param} R:{self.r_param} B:{self.b_param} L:{self.l_param} "
