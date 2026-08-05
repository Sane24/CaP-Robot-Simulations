# model_key=claude
# model_id=claude-opus-4-8
# provider=anthropic
# condition=baseline
# profile=empty
# task=L5
# run=3
# scene=['red block', 'green block', 'blue block', 'yellow block']
# command=put the blocks on different corners clockwise starting at the top right corner.
# generated=2026-08-05T02:40:39
# prompt_chars=12494
# tokens_in=5265 tokens_out=137
# seconds=3.3

say('Ok - putting the blocks on different corners clockwise starting at the top right corner')
block_names = parse_obj_name('the blocks', f'objects = {get_obj_names()}')
corners = parse_position(f'the corners clockwise starting at the top right corner with {len(block_names)} points')
for block_name, pos in zip(block_names, corners):
  put_first_on_second(block_name, pos)
