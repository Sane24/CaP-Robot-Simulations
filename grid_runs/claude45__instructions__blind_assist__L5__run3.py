# model_key=claude45
# model_id=claude-opus-4-5
# provider=anthropic
# condition=instructions
# profile=blind_assist
# task=L5
# run=3
# scene=['red block', 'green block', 'blue block', 'yellow block']
# command=put the blocks on different corners clockwise starting at the top right corner.
# generated=2026-08-05T06:48:31
# prompt_chars=12832
# tokens_in=4112 tokens_out=234
# seconds=7.4

say('Putting the blocks on different corners clockwise starting at the top right corner')
block_names = parse_obj_name('the blocks', f'objects = {get_obj_names()}')
corners = ['top right corner', 'bottom right corner', 'bottom left corner', 'top left corner']
for block_name, corner in zip(block_names, corners):
  corner_pos = parse_position(corner)
  say(f'Placing {block_name} on the {corner}')
  put_first_on_second(block_name, corner_pos)
  actual_pos = get_obj_pos(block_name)
  if np.linalg.norm(np.array(actual_pos) - np.array(corner_pos)) < 0.05:
    say(f'Success: {block_name} is now on the {corner}')
  else:
    say(f'Failed: {block_name} did not reach the {corner}')
