# model=openai condition=baseline profile=none task=T3

purple_block_name = parse_obj_name('purple block', f'objects = {get_obj_names()}')
if purple_block_name:
  say('Putting the purple block on the green block')
  put_first_on_second(purple_block_name, 'green block')
else:
  say('I don\'t see a purple block')
