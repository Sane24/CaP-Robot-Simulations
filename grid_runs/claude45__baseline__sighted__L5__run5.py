# model_key=claude45
# model_id=claude-opus-4-5
# provider=anthropic
# condition=baseline
# profile=sighted
# task=L5
# run=5
# scene=['red block', 'green block', 'blue block', 'yellow block']
# command=put the blocks on different corners clockwise starting at the top right corner.
# generated=2026-08-05T03:44:13
# prompt_chars=12529
# tokens_in=4046 tokens_out=116
# seconds=5.8

say('Placing blocks on corners clockwise starting from the top right')
corners = ['top right corner', 'bottom right corner', 'bottom left corner', 'top left corner']
block_names = parse_obj_name('the blocks', f'objects = {get_obj_names()}')
for block_name, corner in zip(block_names, corners):
  corner_pos = parse_position(corner)
  put_first_on_second(block_name, corner_pos)
