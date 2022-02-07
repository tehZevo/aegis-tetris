from nes_py.wrappers import JoypadSpace
import gym_tetris
from gym_tetris.actions import SIMPLE_MOVEMENT
import numpy as np
import cv2
from protopost import ProtoPost
from nd_to_json import nd_to_json

#TODO: env vars
PORT = 80
REWARD = "lines" #or score
PENALIZE_HEIGHT = False
RENDER = True

#if render, then not threaded
THREADED = not RENDER

#choose game version based on reward criteria
V = 0
if REWARD == "lines":
  V += 1
if PENALIZE_HEIGHT:
  V += 2
env = gym_tetris.make(f"TetrisA-v{V}")
env = JoypadSpace(env, SIMPLE_MOVEMENT)

#scale to 1-pixel-per-mino and make 1.0 = full block, 0.0 = empty block
def scale_state(state):
  state = state[48:-32, 96:-80]
  state = cv2.resize(state, (10, 20))
  state = cv2.cvtColor(state, cv2.COLOR_BGR2GRAY)
  state = state / 255.
  state = np.where(np.greater(state, 0), 1.0, 0.0)
  return state

#https://github.com/Kautenja/gym-tetris/blob/master/gym_tetris/actions.py
#[noop, a, b, right, left, down]
state = env.reset()
state = scale_state(state)

def step(action):
  state, reward, done, info = env.step(action)

  if done:
    state = env.reset()

  if RENDER:
    env.render()

  state = scale_state(state)

  return {
      "obs": nd_to_json(state),
      "done": done,
      "reward": float(reward),
      "info": {} #TODO
    }

routes = {
  "": step,
  "obs": lambda _: nd_to_json(state)
}

ProtoPost(routes).start(PORT, threaded=False)
