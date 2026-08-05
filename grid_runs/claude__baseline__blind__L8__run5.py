# model_key=claude
# model_id=claude-opus-4-8
# provider=anthropic
# condition=baseline
# profile=blind
# task=L8
# run=5
# scene=['red block', 'green block', 'blue block', 'red bowl', 'green bowl', 'blue bowl']
# command=place the blocks in bowls with non-matching colors.
# generated=2026-08-05T02:44:04
# prompt_chars=12522
# tokens_in=5285 tokens_out=135
# seconds=2.3

blocks = parse_obj_name('the blocks', f'objects = {get_obj_names()}')
matches = {'red block': 'green bowl', 'green block': 'blue bowl', 'blue block': 'red bowl'}
say('Ok - placing the blocks in bowls with non-matching colors')
for first, second in matches.items():
  put_first_on_second(first, get_obj_pos(second))
