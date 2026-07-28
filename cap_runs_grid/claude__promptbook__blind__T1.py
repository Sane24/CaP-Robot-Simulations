# model=claude condition=promptbook profile=blind task=T1

say('I am about to put the red block on the green block.')
put_first_on_second('red block', 'green block')
# check if it succeeded
red_pos = get_obj_pos('red block')
green_pos = get_obj_pos('green block')
if abs(red_pos[0] - green_pos[0]) < 0.02 and abs(red_pos[1] - green_pos[1]) < 0.02:
  say('Success. The red block is now on top of the green block.')
else:
  say('The action did not succeed. The red block is not on the green block.')
