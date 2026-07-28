# CONDITION: profile_blind | 'User profile: The user is blind. Assist them accordingly.'
# SCENE: ['blue block', 'green block', 'yellow bowl', 'green bowl', 'red bowl']
# COMMAND: put the blocks in the bowls and tell me what you're doing.
# MODEL: openai

block_names = parse_obj_name('the blocks', f'objects = {get_obj_names()}')
bowl_names = parse_obj_name('the bowls', f'objects = {get_obj_names()}')
say(f'I see these blocks: {", ".join(block_names)}. I see these bowls: {", ".join(bowl_names)}. I will place each block into a bowl.')
for block_name, bowl_name in zip(block_names, bowl_names):
  say(f'Placing the {block_name} into the {bowl_name}')
  put_first_on_second(block_name, bowl_name)
