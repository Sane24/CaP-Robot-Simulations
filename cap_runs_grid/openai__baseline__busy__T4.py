# model=openai condition=baseline profile=busy task=T4

if parse_question('is the red block to the left of the green block?', f'objects = {get_obj_names()}'):
  say('yes')
else:
  say('no')
