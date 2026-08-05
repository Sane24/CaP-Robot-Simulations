# model_key=claude
# model_id=claude-opus-4-8
# provider=anthropic
# condition=baseline
# profile=sighted
# task=L7
# run=1
# scene=['red block', 'green block', 'blue block', 'red bowl', 'green bowl', 'blue bowl']
# command=put the blocks in a vertical line 20cm long and 10cm below the blue bowl.
# generated=2026-08-05T02:47:56
# prompt_chars=12546
# tokens_in=5298 tokens_out=143
# seconds=2.6

line_pts = parse_position('a vertical line 20cm long and 10cm below the blue bowl')
block_names = parse_obj_name('the blocks', f'objects = {get_obj_names()}')
say('Ok - putting the blocks in a vertical line 20cm long and 10cm below the blue bowl')
for block_name, pt in zip(block_names, line_pts):
  put_first_on_second(block_name, pt)
