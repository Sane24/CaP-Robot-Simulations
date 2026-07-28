# model=claude condition=promptbook profile=none task=T2

say('Ok - stacking all blocks with the red block on top')
order_bottom_to_top = ['green block', 'red block']
stack_objects_in_order(object_names=order_bottom_to_top)
# Verify the stack
red_pos = get_obj_pos('red block')
green_pos = get_obj_pos('green block')
if red_pos[2] > green_pos[2] and abs(red_pos[0] - green_pos[0]) < 0.02 and abs(red_pos[1] - green_pos[1]) < 0.02:
  say('Success - the red block is now stacked on top of the green block')
else:
  say('The stacking may not have succeeded as expected')
