# model=claude condition=promptbook profile=sighted task=T3

if is_obj_visible('purple block'):
  say('Putting the purple block on the green block')
  put_first_on_second('purple block', 'green block')
else:
  say('I don\'t see a purple block')
