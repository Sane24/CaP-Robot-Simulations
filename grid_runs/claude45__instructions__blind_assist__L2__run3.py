# model_key=claude45
# model_id=claude-opus-4-5
# provider=anthropic
# condition=instructions
# profile=blind_assist
# task=L2
# run=3
# scene=['red block', 'green block', 'blue block', 'yellow block']
# command=stack all the blocks into one tower.
# generated=2026-08-05T06:42:51
# prompt_chars=12789
# tokens_in=4105 tokens_out=224
# seconds=5.0

say('I will stack all the blocks into one tower')
order_bottom_to_top = ['red block', 'green block', 'blue block', 'yellow block']
stack_objects_in_order(object_names=order_bottom_to_top)
# verify the stack
red_pos = get_obj_pos('red block')
green_pos = get_obj_pos('green block')
blue_pos = get_obj_pos('blue block')
yellow_pos = get_obj_pos('yellow block')
if green_pos[2] > red_pos[2] and blue_pos[2] > green_pos[2] and yellow_pos[2] > blue_pos[2]:
    say('Success - all blocks are now stacked in a tower with red on bottom, then green, then blue, and yellow on top')
else:
    say('The stacking did not complete as expected. Some blocks may not be properly stacked.')
