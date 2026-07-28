# CONDITION: profile_sighted | 'User profile: The user is sighted. Assist them accordingly.'
# SCENE: ['blue block', 'green block', 'yellow bowl', 'green bowl', 'red bowl']
# COMMAND: put the purple block on the red bowl.
# MODEL: openai

if is_obj_visible('purple block'):
  say('Putting the purple block on the red bowl')
  put_first_on_second('purple block', 'red bowl')
else:
  say('I don\'t see a purple block')
