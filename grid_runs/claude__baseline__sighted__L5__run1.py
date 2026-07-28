# model_key=claude
# model_id=claude-opus-4-8
# provider=anthropic
# condition=baseline
# profile=sighted
# task=L5
# run=1
# scene=['red block', 'green block', 'blue block', 'yellow block']
# command=put the blocks on different corners clockwise starting at the top right corner.
# generated=2026-07-28T09:14:24
# prompt_chars=12529
# tokens_in=5276 tokens_out=137
# seconds=3.5

say('Ok - placing the blocks on different corners clockwise starting at the top right corner')
block_names = parse_obj_name('the blocks', f'objects = {get_obj_names()}')
corners = parse_position(f'the corners clockwise starting at the top right corner with {len(block_names)} points')
for block_name, pos in zip(block_names, corners):
  put_first_on_second(block_name, pos)
