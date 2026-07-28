# model_key=openai
# model_id=gpt-5.2
# provider=openai
# condition=baseline
# profile=blind_assist
# task=L5
# run=1
# scene=['red block', 'green block', 'blue block', 'yellow block']
# command=put the blocks on different corners clockwise starting at the top right corner.
# generated=2026-07-23T13:17:31
# prompt_chars=12570
# tokens_in=3255 tokens_out=100
# seconds=2.8

block_names = parse_obj_name('the blocks', f'objects = {get_obj_names()}')
corner_cycle = ['top right corner', 'bottom right corner', 'bottom left corner', 'top left corner']
corners = [parse_position(name) for name in corner_cycle]
say('Ok - placing the blocks on different corners clockwise starting at the top right corner')
for block_name, pos in zip(block_names, corners):
  put_first_on_second(block_name, pos)
