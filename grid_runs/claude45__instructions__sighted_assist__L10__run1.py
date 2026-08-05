# model_key=claude45
# model_id=claude-opus-4-5
# provider=anthropic
# condition=instructions
# profile=sighted_assist
# task=L10
# run=1
# scene=['lemon', 'bottle', 'green plate', 'blue plate']
# command=move all fruits to the green plate and bottles to the blue plate.
# generated=2026-08-05T06:56:09
# prompt_chars=12810
# tokens_in=4111 tokens_out=129
# seconds=2.7

say('Moving all fruits to the green plate and bottles to the blue plate')
fruit_names = parse_obj_name('the fruits', f'objects = {get_obj_names()}')
for fruit_name in fruit_names:
  put_first_on_second(fruit_name, 'green plate')
bottle_names = parse_obj_name('the bottles', f'objects = {get_obj_names()}')
for bottle_name in bottle_names:
  put_first_on_second(bottle_name, 'blue plate')
