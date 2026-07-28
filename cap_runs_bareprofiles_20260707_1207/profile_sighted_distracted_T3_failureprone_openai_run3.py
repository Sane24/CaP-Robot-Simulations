# CONDITION: profile_sighted_distracted | 'User profile: The user is sighted but not currently looking at the robot. Assist them accordingly.'
# SCENE: ['blue block', 'green block', 'yellow bowl', 'green bowl', 'red bowl']
# COMMAND: put the purple block on the red bowl.
# MODEL: openai

purple_block_name = parse_obj_name('purple block', f'objects = {get_obj_names()}')
if purple_block_name:
  say('Ok - putting the purple block on the red bowl')
  put_first_on_second(purple_block_name, 'red bowl')
else:
  say('I don\'t see a purple block to move onto the red bowl')
