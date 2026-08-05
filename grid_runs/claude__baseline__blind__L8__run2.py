# model_key=claude
# model_id=claude-opus-4-8
# provider=anthropic
# condition=baseline
# profile=blind
# task=L8
# run=2
# scene=['red block', 'green block', 'blue block', 'red bowl', 'green bowl', 'blue bowl']
# command=place the blocks in bowls with non-matching colors.
# generated=2026-08-05T02:43:57
# prompt_chars=12522
# tokens_in=5285 tokens_out=106
# seconds=2.0

say('Ok - placing the blocks in bowls with non-matching colors')
non_matches = {'red block': 'green bowl', 'green block': 'blue bowl', 'blue block': 'red bowl'}
for first, second in non_matches.items():
  put_first_on_second(first, get_obj_pos(second))
