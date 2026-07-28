# model_key=openai
# model_id=gpt-5.2
# provider=openai
# condition=baseline
# profile=baseline
# task=L5
# run=1
# scene=['red block', 'green block', 'blue block', 'yellow block']
# command=put the blocks on different corners clockwise starting at the top right corner.
# generated=2026-07-23T13:15:50
# prompt_chars=12494
# tokens_in=3241 tokens_out=136
# seconds=2.8

block_names = parse_obj_name('the blocks', f'objects = {get_obj_names()}')
corners = parse_position('the corners')
top_right_pos = parse_position('top right corner')
corner_order = [top_right_pos]
for pos in corners:
  if not (isinstance(pos, str) and pos == 'top right corner') and not np.allclose(np.array(pos), np.array(top_right_pos)):
    corner_order.append(pos)
say('Ok - putting the blocks on different corners clockwise starting at the top right corner')
for block_name, pos in zip(block_names, corner_order):
  put_first_on_second(block_name, pos)
