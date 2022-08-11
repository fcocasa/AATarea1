from abc import ABC, abstractmethod

from training.l1_train import L1Train

class GXL1Train(L1Train):
    """
    Train is done in this class. You will need to adapt this class to your needs.
    """

    def __init__(self, environment, algorithm, model, **kwargs):
        super().__init__(environment, algorithm, model)

        # We add max_runs and max_steps paramaters
        self.max_runs = kwargs.get('max_runs', 1)
        self.max_steps = kwargs.get('max_steps', 20)

        # TODO: Add more parameters if necessary

    def run(self):
        """
        Runs max_runs episodes, where the agent performs at most max_steps actions. 
        In this implementation, the model is adjusted after each episode, but feel free to change it.
        """

        # Go for max_runs episodes
        for i_run in range(0, self.max_runs):

            # Restart the environment
            observation = self.environment.reset()

            # Go for max_steps per experiment (actually, this cna be set in the env directly)
            experiences = []
            for i_step in range(0, self.max_steps):

                # Do a step in this world
                experience = self.collect_experience(observation)

                # Store the experience for learning
                experiences.append(experience)

                print(f"run:{i_run} step:{i_step} pos:{self.environment.agent_pos} dir:{self.environment.agent_dir} done:{experience['done']} X:{experience['X']}")

                # We finished before reaching max_steps
                if experience['done']:
                    print(f"Run {i_run} finished - reward {experience['next_value']}")
                    break

                # change the observation state
                observation = experience['next_observation']

            # Let's update the agente after each episode
            # TODO: change this to wherever you need
            self.model = self.algorithm.fit(self.model, experiences)

        return self.model

        
        


                








