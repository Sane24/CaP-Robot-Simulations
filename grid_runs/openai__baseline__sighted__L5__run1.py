# model_key=openai
# model_id=gpt-5.2
# provider=openai
# condition=baseline
# profile=sighted
# task=L5
# run=1
# scene=['red block', 'green block', 'blue block', 'yellow block']
# command=put the blocks on different corners clockwise starting at the top right corner.
# generated=2026-07-23T13:16:59
# prompt_chars=12529
# tokens_in=3249 tokens_out=111
# seconds=2.1

block_names = parse_obj_name('the blocks', f'objects = {get_obj_names()}')
corners = parse_position('the corners')
corner_names = ['top right corner', 'bottom right corner', 'bottom left corner', 'top left corner']
corner_pts = [parse_position(cn) for cn in corner_names]
say('Ok - putting the blocks on different corners clockwise starting at the top right corner')
for block_name, pos in zip(block_names, corner_pts):
  put_first_on_second(block_name, pos)
