# model=claude condition=promptbook profile=blind_bare task=T2

say('I am about to stack all the blocks with the red block on top')
order_bottom_to_top = ['green block', 'red block']
stack_objects_in_order(object_names=order_bottom_to_top)
# verify the stack
red_pos = get_obj_pos('red block')
green_pos = get_obj_pos('green block')
if red_pos[1] > green_pos[1] and abs(red_pos[0] - green_pos[0]) < 0.05:
  say('Success - the blocks are stacked with the red block on top')
else:
  say('The stacking did not succeed as expected')
