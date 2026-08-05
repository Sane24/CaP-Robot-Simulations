# model_key=claude
# model_id=claude-opus-4-8
# provider=anthropic
# condition=baseline
# profile=blind
# task=L8
# run=3
# scene=['red block', 'green block', 'blue block', 'red bowl', 'green bowl', 'blue bowl']
# command=place the blocks in bowls with non-matching colors.
# generated=2026-08-05T02:44:00
# prompt_chars=12522
# tokens_in=5285 tokens_out=112
# seconds=2.3

non_matching_matches = {'red block': 'green bowl', 'green block': 'blue bowl', 'blue block': 'red bowl'}
say('Ok - placing the blocks in bowls with non-matching colors')
for first, second in non_matching_matches.items():
  put_first_on_second(first, get_obj_pos(second))
