# model_key=claude45
# model_id=claude-opus-4-5
# provider=anthropic
# condition=instructions
# profile=sighted_assist
# task=L5
# run=5
# scene=['red block', 'green block', 'blue block', 'yellow block']
# command=put the blocks on different corners clockwise starting at the top right corner.
# generated=2026-08-05T06:56:41
# prompt_chars=12834
# tokens_in=4113 tokens_out=213
# seconds=3.4

say('Ok - putting the blocks on different corners clockwise starting at the top right corner')
block_names = parse_obj_name('the blocks', f'objects = {get_obj_names()}')
corners = ['top right corner', 'bottom right corner', 'bottom left corner', 'top left corner']
for block_name, corner in zip(block_names, corners):
  corner_pos = parse_position(corner)
  put_first_on_second(block_name, corner_pos)
  actual_pos = get_obj_pos(block_name)
  if np.linalg.norm(np.array(actual_pos) - np.array(corner_pos)) < 0.02:
    say(f'Successfully placed {block_name} on the {corner}')
  else:
    say(f'Failed to place {block_name} on the {corner}')
