# CONDITION: profile_sighted | 'User profile: The user is sighted. Assist them accordingly.'
# SCENE: ['blue block', 'green block', 'yellow bowl', 'green bowl', 'red bowl']
# COMMAND: stack all the blocks with the green block on top.
# MODEL: openai

say('Ok! Stacking all the blocks with the green block on the top')
block_names = parse_obj_name('the blocks', f'objects = {get_obj_names()}')
other_blocks = [b for b in block_names if b != 'green block']
order_bottom_to_top = other_blocks + ['green block']
stack_objects_in_order(object_names=order_bottom_to_top)
