# model=openai condition=promptbook profile=blind_bare task=T3

say('I am about to put the purple block on the green block')
if is_obj_visible('purple block') and is_obj_visible('green block'):
  put_first_on_second('purple block', 'green block')
  if parse_question('is the purple block on the green block', f'objects = {get_obj_names()}'):
    say('Verified: the purple block is on the green block')
  else:
    say('Not verified: the purple block is not on the green block')
else:
  if not is_obj_visible('purple block'):
    say('I do not see a purple block')
  if not is_obj_visible('green block'):
    say('I do not see a green block')
