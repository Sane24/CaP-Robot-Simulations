# model_key=claude
# model_id=claude-opus-4-8
# provider=anthropic
# condition=baseline
# profile=sighted
# task=L7
# run=4
# scene=['red block', 'green block', 'blue block', 'red bowl', 'green bowl', 'blue bowl']
# command=put the blocks in a vertical line 20cm long and 10cm below the blue bowl.
# generated=2026-08-05T02:48:05
# prompt_chars=12546
# tokens_in=5298 tokens_out=146
# seconds=2.6

say('Ok - putting the blocks in a vertical line 20cm long and 10cm below the blue bowl')
line_pts = parse_position('a 20cm vertical line 10cm below the blue bowl with 3 points')
block_names = parse_obj_name('the blocks', f'objects = {get_obj_names()}')
for block_name, pt in zip(block_names, line_pts):
  put_first_on_second(block_name, pt)
