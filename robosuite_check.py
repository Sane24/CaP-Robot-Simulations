"""
robosuite_check.py -- step 0 for Goal 1. Proves RoboSuite runs headless on CPU
and that ground-truth poses + the built-in success check are readable.
Needs: pip install robosuite "mujoco==3.2.3"
Run:   python robosuite_check.py
"""
import numpy as np
import robosuite as suite
from robosuite.controllers import load_composite_controller_config

cfg = load_composite_controller_config(controller="BASIC")
env = suite.make(env_name="Stack", robots="Panda", controller_configs=cfg,
                 has_renderer=False, has_offscreen_renderer=False,
                 use_camera_obs=False, horizon=500)
env.reset()
for _ in range(5):
    obs, r, done, info = env.step(np.zeros(env.action_dim))

bidA = env.sim.model.body_name2id("cubeA_main")
bidB = env.sim.model.body_name2id("cubeB_main")
print("cubeA pos:", np.round(env.sim.data.body_xpos[bidA], 3))
print("cubeB pos:", np.round(env.sim.data.body_xpos[bidB], 3))
print("action_dim:", env.action_dim)
print("_check_success():", env._check_success())
env.close()
print("\nOK: RoboSuite runs on CPU, poses + success readable.")
