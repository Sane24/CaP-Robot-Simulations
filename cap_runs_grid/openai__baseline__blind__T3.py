# model=openai condition=baseline profile=blind task=T3

if is_obj_visible('purple block'):
  say('I see the purple block. I am picking it up and placing it directly on top of the green block now.')
  put_first_on_second('purple block', 'green block')
  say('Done. The purple block should now be stacked on the green block.')
else:
  say('I do not see a purple block, so I cannot put it on the green block.')
