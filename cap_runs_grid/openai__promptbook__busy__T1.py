# model=openai condition=promptbook profile=busy task=T1

objects = ['red block', 'green block']
if not is_obj_visible('red block'):
  say('I do not see a red block')
elif not is_obj_visible('green block'):
  say('I do not see a green block')
else:
  say('Putting the red block on the green block')
  put_first_on_second('red block', 'green block')
  if parse_question('is the red block on the green block', f'objects = {get_obj_names()}'):
    say('Succeeded - the red block is on the green block')
  else:
    say('Something went wrong - the red block is not on the green block')
