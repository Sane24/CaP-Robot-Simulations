# model_key=claude
# model_id=claude-opus-4-8
# provider=anthropic
# condition=baseline
# profile=sighted
# task=L5
# run=8
# scene=['red block', 'green block', 'blue block', 'yellow block']
# command=put the blocks on different corners clockwise starting at the top right corner.
# generated=2026-07-28T12:07:42
# prompt_chars=12529
# tokens_in=5276 tokens_out=136
# seconds=3.3

order = parse_obj_name('the blocks ordered clockwise starting from the top right corner', f'objects = {get_obj_names()}')
corners = parse_position('the corners clockwise starting at the top right corner')
say('Ok - putting the blocks on the corners clockwise starting at the top right corner')
for block_name, pos in zip(order, corners):
  put_first_on_second(block_name, pos)
