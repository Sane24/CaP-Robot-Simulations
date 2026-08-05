# model_key=claude
# model_id=claude-opus-4-8
# provider=anthropic
# condition=baseline
# profile=sighted
# task=L5
# run=1
# scene=['red block', 'green block', 'blue block', 'yellow block']
# command=put the blocks on different corners clockwise starting at the top right corner.
# generated=2026-08-05T02:48:55
# prompt_chars=12529
# tokens_in=5276 tokens_out=173
# seconds=3.2

order_top_to_bottom = ['top right corner', 'bottom right corner', 'bottom left corner', 'top left corner']
say('Ok - placing the blocks on different corners clockwise starting at the top right corner')
block_names = parse_obj_name('the blocks', f'objects = {get_obj_names()}')
for block_name, corner_name in zip(block_names, order_top_to_bottom):
  corner_pos = parse_position(corner_name)
  put_first_on_second(block_name, corner_pos)
