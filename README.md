Some examples of how to use gym and gym-minigrid.


====================================
INSTALL

You will need gym and gym-minigrid

Gym (0.25.1) can be install directly using pip3: pip3 install gym
There are some compatibility issues, so install gym-minigrid manually from: https://github.com/Farama-Foundation/gym-minigrid

    git clone https://github.com/maximecb/gym-minigrid.git
    cd gym-minigrid
    pip3 install -e .



====================================
EXAMPLES

You will find:

- run_me.py, which shows how to read the different variables around mini-grid world (position, objects, rewards, etc.)

- train.py, and example of how to train a model (it will show the results of the dummy implementation)

- test.py, will show the results of the train model, in a GUI if you like 

They will run without arguments, but, please, check them and try them with different values. In particular, try different mini-grid worlds.



====================================
IMPLEMENTATION

You will need to implement the algorithm, model and training method... Copy the classes GXL1Algo, GXL1Model and GXL1Train, rename it with your group number
 (for example, for group 99 classes will be renamed as G99L1Algo, G99L1Model, G99L1Train) and implement missing parts or adapt the code for your needs.