# CONDITION: profile_blind | 'User profile: The user is blind. Assist them accordingly.'
# SCENE: ['blue block', 'green block', 'yellow bowl', 'green bowl', 'red bowl']
# COMMAND: is the blue block to the left of the green bowl?
# MODEL: openai

if parse_question('is the blue block to the left of the green bowl?', f'objects = {get_obj_names()}'):
  say('yes, the blue block is to the left of the green bowl')
else:
  say('no, the blue block is not to the left of the green bowl')
