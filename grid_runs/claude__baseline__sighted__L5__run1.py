# model_key=claude
# model_id=claude-opus-4-5
# provider=anthropic
# condition=baseline
# profile=sighted
# task=L5
# run=1
# scene=['red block', 'green block', 'blue block', 'yellow block']
# command=put the blocks on different corners clockwise starting at the top right corner.
# generated=2026-07-23T13:13:47
# prompt_chars=12529
# tokens_in=4046 tokens_out=119
# seconds=2.6

say('Putting the blocks on different corners clockwise starting at the top right corner')
block_names = parse_obj_name('the blocks', f'objects = {get_obj_names()}')
corners = ['top right corner', 'bottom right corner', 'bottom left corner', 'top left corner']
for block_name, corner in zip(block_names, corners):
  corner_pos = parse_position(corner)
  put_first_on_second(block_name, corner_pos)
