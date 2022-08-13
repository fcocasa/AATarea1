#!/usr/bin/env python3

import argparse
from ast import arg
from xmlrpc.client import Boolean
from models.g08_l1_model import G08L1Model
from algos.g08_l1_algo import G08L1Algo
from training.g08_l1_train import G08L1Train

import gym 
import time

# This will register the gym_minigrid envs
from gym_minigrid import envs, wrappers


DEFAULT_ENV = 'MiniGrid-Empty-8x8-v0'

# Let's get the arguments
parser = argparse.ArgumentParser()
parser.add_argument("--model", type=str, default=None, required=False, help=F"Model name)")
parser.add_argument("--env", type=str, default=DEFAULT_ENV, required=False, help=F"Name of the environment (default: {DEFAULT_ENV})")
parser.add_argument("--runs", type=int, default=2, required=False, help="Number of experiment runs (default: 2)")
parser.add_argument("--steps", type=int, default=20, required=False, help="Number of max steps per run (default: 20)")
parser.add_argument("--seed", type=int, default=-1, required=False, help="Env seed (default: None)")
parser.add_argument("--gui", type=Boolean, default=False, required=False, help="Show GUI (default: False)")
parser.add_argument("--cheat", type=Boolean, default=False, required=False, help="Use a fixed list of actions (default: False)")

args = parser.parse_args()

print (f"\n\n********** Testing over {args.env} for {args.runs} runs with {args.steps} max steps **********\n\n")

# Create the environment
seed = None if args.seed == -1 else args.seed
environment = gym.make(args.env, seed=seed, render_mode="human")
environment.max_steps = args.steps
environment = wrappers.SymbolicObsWrapper(environment)


m_kargs = {'cheat_mode': args.cheat}
if args.model:
    m_kargs['model'] = args.model
trained_model = G08L1Model(environment, **m_kargs)

for i_run in range(0, args.runs):
    obs = environment.reset()
    reward = 0

    for i_step in range(0,args.steps):
        next_action = trained_model.action(obs)
        obs, reward, done, info = environment.step(next_action)

        if args.gui:
            environment.render()
            time.sleep(0.1)

        if done:
            break

    print(f"Game over with reward {reward}")
    
    if args.gui:
        time.sleep(2)


