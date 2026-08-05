# model_key=claude45
# model_id=claude-opus-4-5
# provider=anthropic
# condition=baseline
# profile=sighted_assist
# task=L5
# run=1
# scene=['red block', 'green block', 'blue block', 'yellow block']
# command=put the blocks on different corners clockwise starting at the top right corner.
# generated=2026-08-05T03:51:43
# prompt_chars=12572
# tokens_in=4054 tokens_out=102
# seconds=10.3

corners = parse_position('the corners starting from the top right corner going clockwise')
block_names = parse_obj_name('the blocks', f'objects = {get_obj_names()}')
say('Putting the blocks on different corners clockwise starting at the top right corner')
for block_name, corner_pos in zip(block_names, corners):
  put_first_on_second(block_name, corner_pos)
