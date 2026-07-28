# model=openai condition=promptbook profile=blind task=T1

objects = ['red block', 'green block']
say('I am about to put the red block on the green block.')
if is_obj_visible('red block') and is_obj_visible('green block'):
  put_first_on_second('red block', 'green block')
  if parse_question('is the red block on the green block', f'objects = {get_obj_names()}'):
    say('I checked: the red block is now on the green block. It worked.')
  else:
    say('I checked: the red block is not on the green block. It did not work.')
else:
  if not is_obj_visible('red block') and not is_obj_visible('green block'):
    say('I cannot do that because I do not see the red block or the green block.')
  elif not is_obj_visible('red block'):
    say('I cannot do that because I do not see the red block.')
  else:
    say('I cannot do that because I do not see the green block.')
