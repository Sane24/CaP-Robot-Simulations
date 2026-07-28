# CONDITION: profile_sighted_distracted | 'User profile: The user is sighted but not currently looking at the robot.'
# SCENE: ['blue block', 'green block', 'yellow bowl', 'green bowl', 'red bowl']
# COMMAND: stack all the blocks with the green block on top.
# MODEL: openai

block_names = parse_obj_name('the blocks', f'objects = {get_obj_names()}')
block_names = [b for b in block_names if b != 'green block']
order_bottom_to_top = block_names + ['green block']
say('Ok! Stacking all the blocks with the green block on the top')
stack_objects_in_order(object_names=order_bottom_to_top)
