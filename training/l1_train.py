from abc import ABC, abstractmethod


class L1Train(ABC):
    """
    Train is done in this class. You should not touch this class, but adapt G08L1Train to your needs.
    """

    def __init__(self, environment,  algorithm, model):
        """
        Initializes a `L1Train` instance. You wont' need to modify this

        Parameters:
        ----------
        environment : gym.Env
            an environment
        algorithm: algos.l1_algo
            the algorithm
        model : models.L1Model
            the model
        """

        # Store parameters
        self.environment = environment
        self.algorithm = algorithm
        self.model = model

######################################################################################
######################################################################################
    def collect_experience_random(self, observation):
            """
            Performs one step in the given environment and returs the result of such experience

            Parameters:
            ----------
            observation : last observation obtained

            Returns
            -------
            exp :  dictionary with the result of asking an action to the model for the given observation and 
            see the result in the given environment 
            """

            # Choose next action
            start_value = self.model.evaluate(observation, self.environment.agent_pos, self.environment.agent_dir)
            action = self.model.action(observation, self.environment,1) #radom move, tipo 1

            # Perform the action
            # Reward es un valor entre 0 y 1 que indica que tan rapido se llegó a destino
            next_observation, reward, done, _ = self.environment.step(action)

            # Add advantage and return to experiences
            next_value = self.model.evaluate(next_observation, self.environment.agent_pos, self.environment.agent_dir)

            exp = {
                'observation': observation,
                'agent_pos': self.environment.agent_pos,
                'agent_dir': self.environment.agent_dir,
                'value': start_value,
                'action': action,
                'next_observation': next_observation,
                'next_value': reward if done else next_value,
                'done': done,
                'reward': reward
            }

            return exp

######################################################################################
######################################################################################

    def collect_experience(self, observation):
        """
        Performs one step in the given environment and returs the result of such experience

        Parameters:
        ----------
        observation : last observation obtained

        Returns
        -------
        exp :  dictionary with the result of asking an action to the model for the given observation and 
        see the result in the given environment 
        """

        # Choose next action
        start_value = self.model.evaluate(observation, self.environment.agent_pos, self.environment.agent_dir)
        action = self.model.action(observation, self.environment, 0)

        # Perform the action
        # Reward es un valor entre 0 y 1 que indica que tan rapido se llegó a destino
        next_observation, reward, done, _ = self.environment.step(action)

        # Add advantage and return to experiences
        next_value = self.model.evaluate(next_observation, self.environment.agent_pos, self.environment.agent_dir)

        exp = {
            'observation': observation,
            'agent_pos': self.environment.agent_pos,
            'agent_dir': self.environment.agent_dir,
            'value': start_value,
            'action': action,
            'next_observation': next_observation,
            'next_value': reward if done else next_value,
            'done': done,
            'reward': reward
        }

        return exp

    @abstractmethod
    def run(self):
        """
        Trains the model. You need to implement it in your the G08L1Train class.
        """

        pass
