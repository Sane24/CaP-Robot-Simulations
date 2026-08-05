# model_key=claude45
# model_id=claude-opus-4-5
# provider=anthropic
# condition=instructions
# profile=blind
# task=L5
# run=4
# scene=['red block', 'green block', 'blue block', 'yellow block']
# command=put the blocks on different corners clockwise starting at the top right corner.
# generated=2026-08-05T06:26:01
# prompt_chars=12789
# tokens_in=4104 tokens_out=218
# seconds=3.4

say('Ok - placing blocks on different corners clockwise starting at the top right corner')
corners = [parse_position('top right corner'), parse_position('bottom right corner'), parse_position('bottom left corner'), parse_position('top left corner')]
block_names = parse_obj_name('the blocks', f'objects = {get_obj_names()}')
for block_name, corner_pos in zip(block_names, corners):
  put_first_on_second(block_name, corner_pos)
  actual_pos = get_obj_pos(block_name)
  if np.linalg.norm(np.array(actual_pos) - np.array(corner_pos)) < 0.02:
    say(f'Successfully placed {block_name} at {get_corner_name(corner_pos)}')
  else:
    say(f'Failed to place {block_name} at the intended corner')
