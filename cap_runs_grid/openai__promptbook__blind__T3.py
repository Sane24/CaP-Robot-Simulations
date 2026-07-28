# model=openai condition=promptbook profile=blind task=T3

say('I am going to check whether a purple block is visible, and if it is, I will place it on the green block.')
if is_obj_visible('purple block'):
  say('I see the purple block. I am going to move it onto the green block now.')
  put_first_on_second('purple block', 'green block')
  if parse_question('is the purple block on the green block', f'objects = {get_obj_names()}'):
    say('Verified: the purple block is on the green block.')
  else:
    say('I moved the purple block, but I cannot verify that it is on the green block.')
else:
  say('I do not see a purple block, so I cannot move it.')
