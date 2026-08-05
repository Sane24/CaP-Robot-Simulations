# model_key=claude45
# model_id=claude-opus-4-5
# provider=anthropic
# condition=baseline
# profile=blind
# task=L5
# run=3
# scene=['red block', 'green block', 'blue block', 'yellow block']
# command=put the blocks on different corners clockwise starting at the top right corner.
# generated=2026-08-05T03:40:12
# prompt_chars=12527
# tokens_in=4045 tokens_out=116
# seconds=4.4

say('Ok - putting blocks on corners clockwise starting from top right')
corners = ['top right corner', 'bottom right corner', 'bottom left corner', 'top left corner']
block_names = parse_obj_name('the blocks', f'objects = {get_obj_names()}')
for block_name, corner in zip(block_names, corners):
  corner_pos = parse_position(corner)
  put_first_on_second(block_name, corner_pos)
