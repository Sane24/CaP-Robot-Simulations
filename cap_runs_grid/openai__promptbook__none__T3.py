# model=openai condition=promptbook profile=none task=T3

say('I am about to check whether a purple block is present; if it is, I will put it on the green block, then verify the result.')
objects = get_obj_names()
if 'purple block' in objects:
  if 'green block' in objects:
    put_first_on_second('purple block', 'green block')
    if parse_question('is the purple block on the green block', f'objects = {get_obj_names()}'):
      say('Verified: the purple block is on the green block.')
    else:
      say('Not verified: the purple block is not on the green block.')
  else:
    say('I do not see a green block.')
else:
  say('I do not see a purple block.')
