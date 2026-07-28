# model=openai condition=promptbook profile=none task=T1

say('I am about to put the red block on the green block.')
objs = get_obj_names()
if ('red block' in objs) and ('green block' in objs) and is_obj_visible('red block') and is_obj_visible('green block'):
  put_first_on_second('red block', 'green block')
  if parse_question('is the red block on the green block', f'objects = {get_obj_names()}'):
    say('Verified: the red block is on the green block.')
  else:
    say('Not verified: the red block is not on the green block.')
else:
  if ('red block' not in objs) or (not is_obj_visible('red block')):
    say('I do not see a red block.')
  if ('green block' not in objs) or (not is_obj_visible('green block')):
    say('I do not see a green block.')
