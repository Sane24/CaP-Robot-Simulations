# model_key=claude
# model_id=claude-opus-4-8
# provider=anthropic
# condition=baseline
# profile=sighted_assist
# task=L8
# run=2
# scene=['red block', 'green block', 'blue block', 'red bowl', 'green bowl', 'blue bowl']
# command=place the blocks in bowls with non-matching colors.
# generated=2026-08-05T02:57:17
# prompt_chars=12567
# tokens_in=5298 tokens_out=106
# seconds=2.1

non_matching = {'red block': 'green bowl', 'green block': 'blue bowl', 'blue block': 'red bowl'}
say('Ok - placing the blocks in bowls with non-matching colors')
for first, second in non_matching.items():
  put_first_on_second(first, get_obj_pos(second))
