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

    def fit(self, model, experiences):
        """ 
        Fits the given model to the new experiences.
        This is your algorithm. You will have to implement everything here
        """
        print('model', model)
        # print('experiences', experiences)
        # TODO: Change this dummy code!

        # Calculate new model parameters from  the experience
        new_value = 0

        # Upadate the model TODO : STOCHASTIC GRADIENT DESCENT (LEAST SQUARES)
        model.update(value=new_value)

        return model
