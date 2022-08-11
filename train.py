#!/usr/bin/env python3

import argparse
from ast import arg
from models.gX_l1_model import GXL1Model
from algos.gX_l1_algo import GXL1Algo
from training.gX_l1_train import GXL1Train

import gym 

# This will register the gym_minigrid envs
from gym_minigrid import envs, wrappers

DEFAULT_ENV = 'MiniGrid-Empty-8x8-v0'

# Let's get the arguments
parser = argparse.ArgumentParser()
parser.add_argument("--env", type=str, default=DEFAULT_ENV, required=False, help=F"Name of the environment (default: {DEFAULT_ENV})")
parser.add_argument("--runs", type=int, default=2, required=False, help="Number of experiment runs (default: 2)")
parser.add_argument("--steps", type=int, default=20, required=False, help="Number of max steps per run (default: 20)")
parser.add_argument("--seed", type=int, default=-1, required=False, help="Env seed (default: None)")

args = parser.parse_args()

print (f"\n\n********** Training over {args.env} for {args.runs} runs with {args.steps} max steps **********\n\n")

seed = None if args.seed == -1 else args.seed

environment = gym.make(args.env, seed=seed, render_mode="human")
environment.max_steps = args.steps
environment = wrappers.SymbolicObsWrapper(environment)

training = GXL1Train(environment, GXL1Algo(), GXL1Model(environment, name="gX_model"), max_runs=args.runs, max_steps=args.steps)

trained_model = training.run()
trained_model.save()
