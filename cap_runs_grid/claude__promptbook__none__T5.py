# model=claude condition=promptbook profile=none task=T5

say('I am about to stack the green block on the red block')
order_bottom_to_top = ['red block', 'green block']
stack_objects_in_order(object_names=order_bottom_to_top)
if is_obj_visible('green block') and is_obj_visible('red block'):
  green_pos = get_obj_pos('green block')
  red_pos = get_obj_pos('red block')
  if abs(green_pos[0] - red_pos[0]) < 0.03 and abs(green_pos[1] - red_pos[1]) < 0.03:
    say('Successfully stacked the green block on the red block')
  else:
    say('The stacking did not succeed as expected')
else:
  say('Could not verify the stack - one or both blocks are not visible')
