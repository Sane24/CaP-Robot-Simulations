# model_key=claude45
# model_id=claude-opus-4-5
# provider=anthropic
# condition=instructions
# profile=sighted_assist
# task=L2
# run=2
# scene=['red block', 'green block', 'blue block', 'yellow block']
# command=stack all the blocks into one tower.
# generated=2026-08-05T06:53:49
# prompt_chars=12791
# tokens_in=4106 tokens_out=277
# seconds=5.3

say('Ok - stacking all the blocks into one tower')
block_names = parse_obj_name('the blocks', f'objects = {get_obj_names()}')
stack_objects_in_order(object_names=block_names)
say('Checking if the stack was successful')
# Verify by checking positions
red_pos = get_obj_pos('red block')
green_pos = get_obj_pos('green block')
blue_pos = get_obj_pos('blue block')
yellow_pos = get_obj_pos('yellow block')
positions = [red_pos, green_pos, blue_pos, yellow_pos]
x_coords = [p[0] for p in positions]
y_coords = [p[1] for p in positions]
x_spread = max(x_coords) - min(x_coords)
y_spread = max(y_coords) - min(y_coords)
if x_spread < 0.05 and y_spread < 0.05:
  say('Success - all blocks are stacked into one tower')
else:
  say('The stacking may not have fully succeeded - blocks are not perfectly aligned')
