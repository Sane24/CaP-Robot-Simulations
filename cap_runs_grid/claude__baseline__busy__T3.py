# model=claude condition=baseline profile=busy task=T3

if is_obj_visible('purple block'):
  put_first_on_second('purple block', 'green block')
else:
  say('I don\'t see a purple block')
