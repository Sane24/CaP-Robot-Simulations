# CONDITION: profile_blind_bare | 'User profile: The user is blind.'
# SCENE: ['blue block', 'green block', 'yellow bowl', 'green bowl', 'red bowl']
# COMMAND: put the blocks in the bowls and tell me what you're doing.
# MODEL: openai

block_names = parse_obj_name('the blocks', f'objects = {get_obj_names()}')
for block_name in block_names:
  bowl_name = parse_obj_name(f'the {block_name} bowl', f'objects = {get_obj_names()}')
  if bowl_name:
    say(f'Putting the {block_name} in the {bowl_name}')
    put_first_on_second(block_name, bowl_name)
  else:
    say(f'I do not see a matching bowl for the {block_name}')
