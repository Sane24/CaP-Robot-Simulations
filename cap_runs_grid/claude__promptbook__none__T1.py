# model=claude condition=promptbook profile=none task=T1

say('Ok - putting the red block on the green block')
put_first_on_second('red block', 'green block')
say('Checking if the action succeeded')
if parse_question('is the red block on the green block', f'objects = {get_obj_names()}'):
  say('Success - the red block is now on the green block')
else:
  say('The action did not succeed - the red block is not on the green block')
