# model_key=claude45
# model_id=claude-opus-4-5
# provider=anthropic
# condition=baseline
# profile=blind_assist
# task=L5
# run=5
# scene=['red block', 'green block', 'blue block', 'yellow block']
# command=put the blocks on different corners clockwise starting at the top right corner.
# generated=2026-08-05T03:47:55
# prompt_chars=12570
# tokens_in=4053 tokens_out=139
# seconds=2.6

say('Putting the blocks on different corners clockwise starting at the top right corner')
block_names = parse_obj_name('the blocks', f'objects = {get_obj_names()}')
corners = ['top right corner', 'bottom right corner', 'bottom left corner', 'top left corner']
for block_name, corner in zip(block_names, corners):
  corner_pos = parse_position(corner)
  say(f'Placing the {block_name} on the {corner}')
  put_first_on_second(block_name, corner_pos)
