# model_key=claude
# model_id=claude-opus-4-8
# provider=anthropic
# condition=baseline
# profile=blind_assist
# task=L10
# run=1
# scene=['lemon', 'bottle', 'green plate', 'blue plate']
# command=move all fruits to the green plate and bottles to the blue plate.
# generated=2026-08-05T02:53:09
# prompt_chars=12546
# tokens_in=5288 tokens_out=173
# seconds=2.7

say('Sure - putting all fruits on the green plate and bottles on the blue plate')
fruit_names = parse_obj_name('the fruits', f'objects = {get_obj_names()}')
for fruit_name in fruit_names:
  put_first_on_second(fruit_name, 'green plate')
bottle_names = parse_obj_name('the bottles', f'objects = {get_obj_names()}')
for bottle_name in bottle_names:
  put_first_on_second(bottle_name, 'blue plate')
