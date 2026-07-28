# CONDITION: profile_sighted | 'User profile: The user is sighted. Assist them accordingly.'
# SCENE: ['blue block', 'green block', 'yellow bowl', 'green bowl', 'red bowl']
# COMMAND: put the blocks in the bowls and tell me what you're doing.
# MODEL: openai

block_names = parse_obj_name('the blocks', f'objects = {get_obj_names()}')
bowl_names = parse_obj_name('the bowls', f'objects = {get_obj_names()}')
if len(bowl_names) == 0:
  say('I do not see any bowls to put the blocks into')
else:
  for i, block_name in enumerate(block_names):
    bowl_name = bowl_names[i % len(bowl_names)]
    say(f'Putting the {block_name} in the {bowl_name}')
    put_first_on_second(block_name, bowl_name)
