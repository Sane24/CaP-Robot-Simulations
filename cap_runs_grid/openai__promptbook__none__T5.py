# model=openai condition=promptbook profile=none task=T5

say('I am going to stack the red block on the green block')
if is_obj_visible('red block') and is_obj_visible('green block'):
  put_first_on_second('red block', 'green block')
  if parse_question('is the red block on the green block', f'objects = {get_obj_names()}'):
    say('It succeeded: the red block is on the green block')
  else:
    say('It did not succeed: the red block is not on the green block')
else:
  if not is_obj_visible('red block'):
    say('I do not see the red block')
  if not is_obj_visible('green block'):
    say('I do not see the green block')
