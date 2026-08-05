# model_key=claude
# model_id=claude-opus-4-8
# provider=anthropic
# condition=baseline
# profile=blind
# task=L10
# run=4
# scene=['lemon', 'bottle', 'green plate', 'blue plate']
# command=move all fruits to the green plate and bottles to the blue plate.
# generated=2026-08-05T02:44:36
# prompt_chars=12503
# tokens_in=5276 tokens_out=174
# seconds=3.3

fruit_names = parse_obj_name('the fruits', f'objects = {get_obj_names()}')
bottle_names = parse_obj_name('the bottles', f'objects = {get_obj_names()}')
say('Ok - moving all fruits to the green plate and all bottles to the blue plate')
for fruit_name in fruit_names:
  put_first_on_second(fruit_name, 'green plate')
for bottle_name in bottle_names:
  put_first_on_second(bottle_name, 'blue plate')
