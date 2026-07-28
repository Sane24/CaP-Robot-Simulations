# model=claude condition=promptbook profile=sighted task=T1

say('Ok - putting the red block on the green block')
put_first_on_second('red block', 'green block')
red_block_pos = get_obj_pos('red block')
green_block_pos = get_obj_pos('green block')
if np.allclose(red_block_pos[:2], green_block_pos[:2], atol=0.02) and red_block_pos[2] > green_block_pos[2]:
  say('Success - the red block is now on the green block')
else:
  say('The action did not succeed as expected')
