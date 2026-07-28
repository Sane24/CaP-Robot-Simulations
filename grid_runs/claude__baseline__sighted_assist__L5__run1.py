# model_key=claude
# model_id=claude-opus-4-5
# provider=anthropic
# condition=baseline
# profile=sighted_assist
# task=L5
# run=1
# scene=['red block', 'green block', 'blue block', 'yellow block']
# command=put the blocks on different corners clockwise starting at the top right corner.
# generated=2026-07-23T13:15:08
# prompt_chars=12572
# tokens_in=4054 tokens_out=99
# seconds=2.9

say('Placing the blocks on different corners clockwise starting at the top right corner')
block_names = parse_obj_name('the blocks', f'objects = {get_obj_names()}')
corners = parse_position('the corners in clockwise order starting at the top right corner')
for block_name, pos in zip(block_names, corners):
  put_first_on_second(block_name, pos)
