# model_key=claude
# model_id=claude-opus-4-8
# provider=anthropic
# condition=baseline
# profile=sighted
# task=L8
# run=1
# scene=['red block', 'green block', 'blue block', 'red bowl', 'green bowl', 'blue bowl']
# command=place the blocks in bowls with non-matching colors.
# generated=2026-08-05T02:48:11
# prompt_chars=12524
# tokens_in=5286 tokens_out=106
# seconds=3.4

say('Ok - placing the blocks in bowls with non-matching colors')
non_matches = {'red block': 'green bowl', 'green block': 'blue bowl', 'blue block': 'red bowl'}
for first, second in non_matches.items():
  put_first_on_second(first, get_obj_pos(second))
