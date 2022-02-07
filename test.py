from operator import itemgetter
import cv2
import numpy as np
from protopost import protopost_client as ppcl
from nd_to_json import json_to_nd

import keyboard

cv2.namedWindow("img", cv2.WINDOW_NORMAL)

TETRIS_HOST = "http://127.0.0.1:8080"

TETRIS = lambda action: ppcl(TETRIS_HOST, action)

#[noop, a, b, right, left, down]
def keyboard_action():
  actions = [
    0, #noop
    keyboard.is_pressed("z"), #a
    keyboard.is_pressed("x"), #b
    keyboard.is_pressed("right"),
    keyboard.is_pressed("left"),
    keyboard.is_pressed("down")
  ]
  action = int(np.argmax(actions))
  return action

while True:
  action = keyboard_action()
  # action = np.random.randint(6)
  response = TETRIS(action)
  obs, done, reward, info = itemgetter("obs", "done", "reward", "info")(response)
  obs = json_to_nd(obs)
  cv2.imshow("img", obs)
  cv2.waitKey(1)
  print("reward", reward)
