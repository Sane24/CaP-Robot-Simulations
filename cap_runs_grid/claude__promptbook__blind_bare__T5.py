# model=claude condition=promptbook profile=blind_bare task=T5

say('I am about to stack the green block on the red block')
order_bottom_to_top = ['red block', 'green block']
stack_objects_in_order(object_names=order_bottom_to_top)
# verify the stack
green_pos = get_obj_pos('green block')
red_pos = get_obj_pos('red block')
if green_pos[0] is not None and red_pos[0] is not None:
  if abs(green_pos[0] - red_pos[0]) < 0.05 and abs(green_pos[1] - red_pos[1]) < 0.05:
    say('Success - the green block is now stacked on top of the red block')
  else:
    say('The stacking did not succeed as expected')
else:
  say('Could not verify the positions of the blocks')
