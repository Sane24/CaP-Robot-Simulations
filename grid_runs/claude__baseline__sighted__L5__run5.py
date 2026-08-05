# model_key=claude
# model_id=claude-opus-4-8
# provider=anthropic
# condition=baseline
# profile=sighted
# task=L5
# run=5
# scene=['red block', 'green block', 'blue block', 'yellow block']
# command=put the blocks on different corners clockwise starting at the top right corner.
# generated=2026-08-05T02:49:10
# prompt_chars=12529
# tokens_in=5276 tokens_out=135
# seconds=4.4

order_of_corners = parse_position('the corners in clockwise order starting at the top right corner')
block_names = parse_obj_name('the blocks', f'objects = {get_obj_names()}')
say('Ok - placing the blocks on different corners clockwise starting at the top right corner')
for block_name, pos in zip(block_names, order_of_corners):
  put_first_on_second(block_name, pos)
