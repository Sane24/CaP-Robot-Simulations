# model_key=claude
# model_id=claude-opus-4-8
# provider=anthropic
# condition=baseline
# profile=sighted_assist
# task=L5
# run=8
# scene=['red block', 'green block', 'blue block', 'yellow block']
# command=put the blocks on different corners clockwise starting at the top right corner.
# generated=2026-07-28T12:11:38
# prompt_chars=12572
# tokens_in=5288 tokens_out=137
# seconds=3.9

order_bottom_to_top = parse_obj_name('the blocks', f'objects = {get_obj_names()}')
corners = parse_position('the corners clockwise starting at the top right corner')
say('Ok - putting the blocks on different corners clockwise starting at the top right corner')
for block_name, pos in zip(order_bottom_to_top, corners):
  put_first_on_second(block_name, pos)
