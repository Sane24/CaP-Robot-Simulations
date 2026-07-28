# model=openai condition=promptbook profile=none task=T4

say('I am about to check whether the red block is to the left of the green block.')
result = parse_question('is the red block to the left of the green block?', f'objects = {get_obj_names()}')
if result:
  say('Yes, the red block is to the left of the green block.')
else:
  say('No, the red block is not to the left of the green block.')
