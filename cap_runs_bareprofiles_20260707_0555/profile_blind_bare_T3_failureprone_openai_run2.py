# CONDITION: profile_blind_bare | 'User profile: The user is blind.'
# SCENE: ['blue block', 'green block', 'yellow bowl', 'green bowl', 'red bowl']
# COMMAND: put the purple block on the red bowl.
# MODEL: openai

block_name = parse_obj_name('purple block', f'objects = {get_obj_names()}')
if block_name:
  say('Ok - putting the purple block on the red bowl')
  put_first_on_second(block_name, 'red bowl')
else:
  say('I do not see a purple block')
