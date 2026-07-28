# model=openai condition=promptbook profile=sighted task=T2

objects = get_obj_names()
if (not is_obj_visible('red block')) or (not is_obj_visible('green block')):
  missing = []
  if not is_obj_visible('red block'):
    missing.append('red block')
  if not is_obj_visible('green block'):
    missing.append('green block')
  say(f'I do not see the {", ".join(missing)}')
else:
  say('I am about to stack the blocks with the red block on top')
  pre_pos_green = get_obj_pos('green block')
  pre_pos_red = get_obj_pos('red block')
  stack_objects_in_order(object_names=['green block', 'red block'])
  post_pos_green = get_obj_pos('green block')
  post_pos_red = get_obj_pos('red block')
  if (np.linalg.norm(np.array(post_pos_green) - np.array(pre_pos_green)) > 1e-3) or (np.linalg.norm(np.array(post_pos_red) - np.array(pre_pos_red)) > 1e-3):
    say('I verified the stack action succeeded')
  else:
    say('I checked the scene and the stack action did not succeed')
