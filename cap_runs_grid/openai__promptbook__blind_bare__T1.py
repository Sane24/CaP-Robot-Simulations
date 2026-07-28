# model=openai condition=promptbook profile=blind_bare task=T1

objects = get_obj_names()
if ('red block' in objects) and ('green block' in objects) and is_obj_visible('red block') and is_obj_visible('green block'):
  say('I am about to put the red block on the green block.')
  put_first_on_second('red block', 'green block')
  objects = get_obj_names()
  if parse_question('is the red block on the green block', f'objects = {objects}'):
    say('It succeeded: the red block is on the green block.')
  else:
    say('It did not succeed: the red block is not on the green block.')
else:
  missing = []
  if 'red block' not in objects or (not is_obj_visible('red block')):
    missing.append('red block')
  if 'green block' not in objects or (not is_obj_visible('green block')):
    missing.append('green block')
  say(f'I cannot do that because I do not see the following object(s): {", ".join(missing)}.')
