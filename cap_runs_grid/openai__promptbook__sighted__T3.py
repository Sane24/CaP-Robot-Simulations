# model=openai condition=promptbook profile=sighted task=T3

objects = get_obj_names()
if 'purple block' not in objects:
  say('I am about to put the purple block on the green block, but I do not see a purple block')
elif 'green block' not in objects:
  say('I am about to put the purple block on the green block, but I do not see a green block')
else:
  say('I am about to put the purple block on the green block')
  put_first_on_second('purple block', 'green block')
  if parse_question('is the purple block on the green block', f'objects = {get_obj_names()}'):
    say('It succeeded: the purple block is on the green block')
  else:
    say('It did not succeed: the purple block is not on the green block')
