# model_key=claude
# model_id=claude-opus-4-5
# provider=anthropic
# condition=baseline
# profile=blind
# task=L5
# run=1
# scene=['red block', 'green block', 'blue block', 'yellow block']
# command=put the blocks on different corners clockwise starting at the top right corner.
# generated=2026-07-23T13:12:47
# prompt_chars=12527
# tokens_in=4045 tokens_out=119
# seconds=2.1

corners = ['top right corner', 'bottom right corner', 'bottom left corner', 'top left corner']
block_names = parse_obj_name('the blocks', f'objects = {get_obj_names()}')
say('Putting the blocks on different corners clockwise starting at the top right corner')
for block_name, corner in zip(block_names, corners):
  corner_pos = parse_position(corner)
  put_first_on_second(block_name, corner_pos)
