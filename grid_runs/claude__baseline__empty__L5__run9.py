# model_key=claude
# model_id=claude-opus-4-8
# provider=anthropic
# condition=baseline
# profile=empty
# task=L5
# run=9
# scene=['red block', 'green block', 'blue block', 'yellow block']
# command=put the blocks on different corners clockwise starting at the top right corner.
# generated=2026-07-28T12:03:57
# prompt_chars=12494
# tokens_in=5265 tokens_out=137
# seconds=2.7

say('Ok - putting the blocks on different corners clockwise starting at the top right corner')
block_names = parse_obj_name('the blocks', f'objects = {get_obj_names()}')
corners = parse_position(f'the corners clockwise starting at the top right corner with {len(block_names)} points')
for block_name, pos in zip(block_names, corners):
  put_first_on_second(block_name, pos)
