# model_key=claude45
# model_id=claude-opus-4-5
# provider=anthropic
# condition=instructions
# profile=empty
# task=L3
# run=2
# scene=['red block', 'green block', 'blue block', 'yellow block']
# command=put the blocks in a horizontal line near the top.
# generated=2026-08-05T06:13:53
# prompt_chars=12726
# tokens_in=4091 tokens_out=191
# seconds=10.1

say('Ok - making a horizontal line of blocks near the top')
block_names = parse_obj_name('the blocks', f'objects = {get_obj_names()}')
line_pts = parse_position(f'a 30cm horizontal line near the top with {len(block_names)} points')
for block_name, pt in zip(block_names, line_pts):
  put_first_on_second(block_name, pt)
  actual_pos = get_obj_pos(block_name)
  if np.linalg.norm(np.array(actual_pos) - np.array(pt)) < 0.02:
    say(f'Successfully placed {block_name}')
  else:
    say(f'Failed to place {block_name} at target position')
