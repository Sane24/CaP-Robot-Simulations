# model_key=openai
# model_id=gpt-5.2
# provider=openai
# condition=baseline
# profile=blind_assist
# task=L5
# run=2
# scene=['red block', 'green block', 'blue block', 'yellow block']
# command=put the blocks on different corners clockwise starting at the top right corner.
# generated=2026-07-23T13:17:34
# prompt_chars=12570
# tokens_in=3255 tokens_out=157
# seconds=2.9

block_names = parse_obj_name('the blocks', f'objects = {get_obj_names()}')
corner_positions = parse_position('the corners')
top_right_pos = parse_position('top right corner')
top_right_idx = int(np.argmin([np.linalg.norm(np.array(pos) - np.array(top_right_pos)) for pos in corner_positions]))
corner_positions_clockwise = corner_positions[top_right_idx:] + corner_positions[:top_right_idx]
say('Ok - placing the blocks on corners clockwise starting at the top right corner')
for block_name, corner_pos in zip(block_names, corner_positions_clockwise):
  say(f'Placing the {block_name} on the {get_corner_name(corner_pos)}')
  put_first_on_second(block_name, corner_pos)
