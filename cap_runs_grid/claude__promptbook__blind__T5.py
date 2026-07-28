# model=claude condition=promptbook profile=blind task=T5

say('I am about to stack the green block on top of the red block. First, I will place the red block, then stack the green block on it.')
order_bottom_to_top = ['red block', 'green block']
stack_objects_in_order(object_names=order_bottom_to_top)
# verify the stack
red_pos = get_obj_pos('red block')
green_pos = get_obj_pos('green block')
if green_pos[1] > red_pos[1] - 0.02 and abs(green_pos[0] - red_pos[0]) < 0.03:
    say('Success. The green block is now stacked on top of the red block.')
else:
    say('The stacking did not work as expected. The blocks may not be properly aligned.')
