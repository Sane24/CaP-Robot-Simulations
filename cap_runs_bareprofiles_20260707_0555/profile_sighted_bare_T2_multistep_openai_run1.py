# CONDITION: profile_sighted_bare | 'User profile: The user is sighted.'
# SCENE: ['blue block', 'green block', 'yellow bowl', 'green bowl', 'red bowl']
# COMMAND: stack all the blocks with the green block on top.
# MODEL: openai

block_names = parse_obj_name('the blocks', f'objects = {get_obj_names()}')
block_names = [b for b in block_names if b != 'green block'] + ['green block']
say('Ok! Stacking all the blocks with the green block on top')
stack_objects_in_order(object_names=block_names)
