# model_key=claude45
# model_id=claude-opus-4-5
# provider=anthropic
# condition=instructions
# profile=blind_assist
# task=L2
# run=5
# scene=['red block', 'green block', 'blue block', 'yellow block']
# command=stack all the blocks into one tower.
# generated=2026-08-05T06:43:01
# prompt_chars=12789
# tokens_in=4105 tokens_out=346
# seconds=6.2

say('I will now stack all blocks into one tower.')
order_bottom_to_top = ['red block', 'green block', 'blue block', 'yellow block']
stack_objects_in_order(object_names=order_bottom_to_top)
# verify the stack
red_pos = get_obj_pos('red block')
green_pos = get_obj_pos('green block')
blue_pos = get_obj_pos('blue block')
yellow_pos = get_obj_pos('yellow block')
success = True
if not (abs(green_pos[0] - red_pos[0]) < 0.03 and abs(green_pos[1] - red_pos[1]) < 0.03):
    success = False
if not (abs(blue_pos[0] - green_pos[0]) < 0.03 and abs(blue_pos[1] - green_pos[1]) < 0.03):
    success = False
if not (abs(yellow_pos[0] - blue_pos[0]) < 0.03 and abs(yellow_pos[1] - blue_pos[1]) < 0.03):
    success = False
if success:
    say('Success. All four blocks are now stacked in a tower with red on the bottom, then green, then blue, and yellow on top.')
else:
    say('The stacking did not succeed as expected. Some blocks may not be aligned properly.')
