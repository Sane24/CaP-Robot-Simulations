# model_key=claude45
# model_id=claude-opus-4-5
# provider=anthropic
# condition=instructions
# profile=blind
# task=L7
# run=3
# scene=['red block', 'green block', 'blue block', 'red bowl', 'green bowl', 'blue bowl']
# command=put the blocks in a vertical line 20cm long and 10cm below the blue bowl.
# generated=2026-08-05T06:24:32
# prompt_chars=12806
# tokens_in=4119 tokens_out=181
# seconds=2.8

say('Putting the blocks in a vertical line 20cm long and 10cm below the blue bowl')
block_names = parse_obj_name('the blocks', f'objects = {get_obj_names()}')
line_pts = parse_position(f'a 20cm vertical line 10cm below the blue bowl with {len(block_names)} points')
for block_name, pt in zip(block_names, line_pts):
  put_first_on_second(block_name, pt)
# verify the placement
for block_name in block_names:
  if is_obj_visible(block_name):
    say(f'Successfully placed {block_name}')
  else:
    say(f'Failed to place {block_name}')
