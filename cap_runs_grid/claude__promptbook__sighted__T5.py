# model=claude condition=promptbook profile=sighted task=T5

say('I am going to stack the blocks with the red block on the bottom and the green block on top')
order_bottom_to_top = ['red block', 'green block']
stack_objects_in_order(object_names=order_bottom_to_top)
if is_obj_visible('green block') and is_obj_visible('red block'):
    green_pos = get_obj_pos('green block')
    red_pos = get_obj_pos('red block')
    if green_pos[1] > red_pos[1]:
        say('Success - the blocks are now stacked with the green block on top of the red block')
    else:
        say('The stacking did not succeed as expected')
else:
    say('Could not verify the stack - one or more blocks are not visible')
