# CONDITION: profile_sighted_distracted | 'User profile: The user is sighted but not currently looking at the robot. Assist them accordingly.'
# SCENE: ['blue block', 'green block', 'yellow bowl', 'green bowl', 'red bowl']
# COMMAND: put the blue block on the yellow bowl.
# MODEL: claude

say('Got it - putting the blue block on the yellow bowl')
put_first_on_second('blue block', 'yellow bowl')
