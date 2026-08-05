# model_key=claude45
# model_id=claude-opus-4-5
# provider=anthropic
# condition=baseline
# profile=blind
# task=L5
# run=1
# scene=['red block', 'green block', 'blue block', 'yellow block']
# command=put the blocks on different corners clockwise starting at the top right corner.
# generated=2026-08-05T03:40:05
# prompt_chars=12527
# tokens_in=4045 tokens_out=98
# seconds=1.9

corners = parse_position('the corners starting at the top right corner going clockwise')
block_names = parse_obj_name('the blocks', f'objects = {get_obj_names()}')
say('Putting the blocks on different corners clockwise starting at the top right corner')
for block_name, corner in zip(block_names, corners):
  put_first_on_second(block_name, corner)
