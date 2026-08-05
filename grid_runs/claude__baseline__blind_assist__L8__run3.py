# model_key=claude
# model_id=claude-opus-4-8
# provider=anthropic
# condition=baseline
# profile=blind_assist
# task=L8
# run=3
# scene=['red block', 'green block', 'blue block', 'red bowl', 'green bowl', 'blue bowl']
# command=place the blocks in bowls with non-matching colors.
# generated=2026-08-05T02:52:41
# prompt_chars=12565
# tokens_in=5297 tokens_out=112
# seconds=2.3

non_matching_matches = {'red block': 'green bowl', 'green block': 'blue bowl', 'blue block': 'red bowl'}
say('Ok - placing the blocks in bowls with non-matching colors')
for first, second in non_matching_matches.items():
  put_first_on_second(first, get_obj_pos(second))
