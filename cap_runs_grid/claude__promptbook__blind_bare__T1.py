# model=claude condition=promptbook profile=blind_bare task=T1

say('About to put the red block on the green block')
put_first_on_second('red block', 'green block')
# verify the action
red_pos = get_obj_pos('red block')
green_pos = get_obj_pos('green block')
if abs(red_pos[0] - green_pos[0]) < 0.05 and abs(red_pos[1] - green_pos[1]) < 0.05:
  say('Success - the red block is now on the green block')
else:
  say('The action did not succeed - the red block is not on the green block')
