# model_key=claude
# model_id=claude-opus-4-8
# provider=anthropic
# condition=baseline
# profile=empty
# task=L8
# run=4
# scene=['red block', 'green block', 'blue block', 'red bowl', 'green bowl', 'blue bowl']
# command=place the blocks in bowls with non-matching colors.
# generated=2026-08-05T02:40:01
# prompt_chars=12489
# tokens_in=5275 tokens_out=107
# seconds=5.4


say('Ok - placing the blocks in bowls with non-matching colors')
non_matches = {'red block': 'green bowl', 'green block': 'blue bowl', 'blue block': 'red bowl'}
for first, second in non_matches.items():
  put_first_on_second(first, get_obj_pos(second))
