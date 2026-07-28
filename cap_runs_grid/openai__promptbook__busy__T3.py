# model=openai condition=promptbook profile=busy task=T3

objects = get_obj_names()
if not is_obj_visible('green block'):
  say('I do not see a green block')
elif not is_obj_visible('purple block'):
  say('I do not see a purple block')
else:
  say('I am going to put the purple block on the green block')
  put_first_on_second('purple block', 'green block')
  if parse_question('is the purple block on the green block', f'objects = {get_obj_names()}'):
    say('It worked: the purple block is on the green block')
  else:
    say('Something went wrong: the purple block is not on the green block')
