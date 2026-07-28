# CONDITION: profile_sighted_bare | 'User profile: The user is sighted.'
# SCENE: ['blue block', 'green block', 'yellow bowl', 'green bowl', 'red bowl']
# COMMAND: put the blue block on the yellow bowl.
# MODEL: openai

say('Ok - putting the blue block on the yellow bowl')
put_first_on_second('blue block', 'yellow bowl')
