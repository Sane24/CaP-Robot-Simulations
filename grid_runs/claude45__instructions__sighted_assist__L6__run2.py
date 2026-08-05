# model_key=claude45
# model_id=claude-opus-4-5
# provider=anthropic
# condition=instructions
# profile=sighted_assist
# task=L6
# run=2
# scene=['red block', 'green block', 'blue block', 'yellow block']
# command=arrange the blocks in a square around the middle.
# generated=2026-08-05T06:55:01
# prompt_chars=12804
# tokens_in=4108 tokens_out=198
# seconds=3.3

say('Arranging the blocks in a square around the middle')
block_names = parse_obj_name('the blocks', f'objects = {get_obj_names()}')
square_pts = parse_position(f'a square with size 10cm around the middle with {len(block_names)} points')
for block_name, pt in zip(block_names, square_pts):
  put_first_on_second(block_name, pt)
  block_pos = get_obj_pos(block_name)
  if np.linalg.norm(np.array(block_pos[:2]) - np.array(pt[:2])) < 0.02:
    say(f'Successfully placed {block_name}')
  else:
    say(f'Failed to place {block_name} at the target position')
