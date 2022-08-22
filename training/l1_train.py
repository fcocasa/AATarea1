from abc import ABC, abstractmethod
import random


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
        self.random_forward = 0.4  # 0 - deterministic, 1 - always moves forward
        self.randomness_cooldown = 0.8

    def collect_experience(self, observation, visibility):
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
        start_value = self.model.evaluate(
            observation, self.environment.agent_pos, self.environment.agent_dir, visibility)
        action = self.model.action(observation, self.environment, visibility)

        if random.uniform(0, 1) <= self.random_forward:
            action = random.choice(
                [self.environment.actions.right, self.environment.actions.forward, self.environment.actions.left])

        # Perform the action
        # Reward es un valor entre 0 y 1 que indica que tan rapido se llegó a destino
        next_observation, reward, done, _ = self.environment.step(action)

        if reward > 0:
            self.random_forward = self.random_forward*self.randomness_cooldown

        # Add advantage and return to experiences
        next_value = self.model.evaluate(
            next_observation, self.environment.agent_pos, self.environment.agent_dir, visibility)

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
