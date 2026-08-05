# model_key=claude
# model_id=claude-opus-4-8
# provider=anthropic
# condition=baseline
# profile=sighted_assist
# task=L8
# run=1
# scene=['red block', 'green block', 'blue block', 'red bowl', 'green bowl', 'blue bowl']
# command=place the blocks in bowls with non-matching colors.
# generated=2026-08-05T02:57:15
# prompt_chars=12567
# tokens_in=5298 tokens_out=104
# seconds=2.2

say('Ok - placing the blocks in bowls with non-matching colors')
non_matching_matches = {'red block': 'green bowl', 'green block': 'blue bowl', 'blue block': 'red bowl'}
for first, second in non_matching_matches.items():
  put_first_on_second(first, second)
