# model_key=claude
# model_id=claude-opus-4-8
# provider=anthropic
# condition=baseline
# profile=blind
# task=L5
# run=1
# scene=['red block', 'green block', 'blue block', 'yellow block']
# command=put the blocks on different corners clockwise starting at the top right corner.
# generated=2026-08-05T02:44:42
# prompt_chars=12527
# tokens_in=5275 tokens_out=137
# seconds=2.8

order_bottom_to_top = parse_obj_name('the blocks', f'objects = {get_obj_names()}')
corners = parse_position('the corners clockwise starting at the top right corner')
say('Ok - placing the blocks on different corners clockwise starting from the top right corner')
for block_name, pos in zip(order_bottom_to_top, corners):
  put_first_on_second(block_name, pos)
