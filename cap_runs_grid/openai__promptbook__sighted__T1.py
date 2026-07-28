# model=openai condition=promptbook profile=sighted task=T1

objects = get_obj_names()
if (not is_obj_visible('red block')) or (not is_obj_visible('green block')):
  say('I do not see the red block or the green block')
else:
  say('I am going to put the red block on the green block')
  put_first_on_second('red block', 'green block')
  objects = get_obj_names()
  if parse_question('is the red block on the green block', f'objects = {objects}'):
    say('It succeeded: the red block is on the green block')
  else:
    say('It did not succeed: the red block is not on the green block')
