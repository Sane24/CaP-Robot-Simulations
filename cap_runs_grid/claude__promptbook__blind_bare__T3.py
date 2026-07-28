# model=claude condition=promptbook profile=blind_bare task=T3

if is_obj_visible('purple block'):
  say('Putting the purple block on the green block')
  put_first_on_second('purple block', 'green block')
  # verify the action
  purple_pos = get_obj_pos('purple block')
  green_pos = get_obj_pos('green block')
  if np.linalg.norm(np.array(purple_pos[:2]) - np.array(green_pos[:2])) < 0.05:
    say('Success - the purple block is now on the green block')
  else:
    say('The action did not succeed - the purple block is not on the green block')
else:
  say('I don\'t see a purple block')
