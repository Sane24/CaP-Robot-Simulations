# model_key=claude
# model_id=claude-opus-4-8
# provider=anthropic
# condition=baseline
# profile=empty
# task=L5
# run=6
# scene=['red block', 'green block', 'blue block', 'yellow block']
# command=put the blocks on different corners clockwise starting at the top right corner.
# generated=2026-07-28T12:03:50
# prompt_chars=12494
# tokens_in=5265 tokens_out=125
# seconds=2.2

say('Ok - putting the blocks on different corners clockwise starting at the top right corner')
block_names = parse_obj_name('the blocks', f'objects = {get_obj_names()}')
corners = parse_position('the corners clockwise starting at the top right corner')
for block_name, pos in zip(block_names, corners):
  put_first_on_second(block_name, pos)
