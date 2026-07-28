# model_key=openai
# model_id=gpt-5.2
# provider=openai
# condition=baseline
# profile=sighted_assist
# task=L5
# run=1
# scene=['red block', 'green block', 'blue block', 'yellow block']
# command=put the blocks on different corners clockwise starting at the top right corner.
# generated=2026-07-23T13:18:01
# prompt_chars=12572
# tokens_in=3256 tokens_out=138
# seconds=2.2

block_names = parse_obj_name('the blocks', f'objects = {get_obj_names()}')
corner_positions = parse_position('the corners')
top_right_corner = parse_position('top right corner')
say('Ok - putting the blocks on different corners clockwise starting at the top right corner')
for i, pos in enumerate(corner_positions):
  if np.allclose(pos, top_right_corner):
    start_idx = i
    break
else:
  start_idx = 0
corner_positions = corner_positions[start_idx:] + corner_positions[:start_idx]
for block_name, pos in zip(block_names, corner_positions):
  put_first_on_second(block_name, pos)
