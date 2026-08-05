# model_key=claude
# model_id=claude-opus-4-8
# provider=anthropic
# condition=baseline
# profile=sighted_assist
# task=L8
# run=3
# scene=['red block', 'green block', 'blue block', 'red bowl', 'green bowl', 'blue bowl']
# command=place the blocks in bowls with non-matching colors.
# generated=2026-08-05T02:57:19
# prompt_chars=12567
# tokens_in=5298 tokens_out=99
# seconds=2.3

say('Placing the blocks in bowls with non-matching colors')
matches = {'red block': 'green bowl', 'green block': 'blue bowl', 'blue block': 'red bowl'}
for first, second in matches.items():
  put_first_on_second(first, get_obj_pos(second))
