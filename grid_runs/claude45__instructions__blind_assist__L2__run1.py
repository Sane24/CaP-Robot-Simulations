# model_key=claude45
# model_id=claude-opus-4-5
# provider=anthropic
# condition=instructions
# profile=blind_assist
# task=L2
# run=1
# scene=['red block', 'green block', 'blue block', 'yellow block']
# command=stack all the blocks into one tower.
# generated=2026-08-05T07:44:18
# prompt_chars=12789
# tokens_in=4105 tokens_out=353
# seconds=12.0

say('I will now stack all the blocks into one tower.')
order_bottom_to_top = ['red block', 'green block', 'blue block', 'yellow block']
stack_objects_in_order(object_names=order_bottom_to_top)
# verify the stack
top_block_pos = get_obj_pos('yellow block')
blue_block_pos = get_obj_pos('blue block')
green_block_pos = get_obj_pos('green block')
red_block_pos = get_obj_pos('red block')
if (abs(top_block_pos[0] - blue_block_pos[0]) < 0.02 and abs(top_block_pos[1] - blue_block_pos[1]) < 0.02 and
    abs(blue_block_pos[0] - green_block_pos[0]) < 0.02 and abs(blue_block_pos[1] - green_block_pos[1]) < 0.02 and
    abs(green_block_pos[0] - red_block_pos[0]) < 0.02 and abs(green_block_pos[1] - red_block_pos[1]) < 0.02):
  say('Success! All blocks are now stacked in a tower with the red block on the bottom, then green, then blue, and yellow on top.')
else:
  say('The stacking did not fully succeed. Some blocks may not be aligned properly.')
