# model_key=claude45
# model_id=claude-opus-4-5
# provider=anthropic
# condition=instructions
# profile=blind
# task=L2
# run=4
# scene=['red block', 'green block', 'blue block', 'yellow block']
# command=stack all the blocks into one tower.
# generated=2026-08-05T06:22:32
# prompt_chars=12746
# tokens_in=4097 tokens_out=156
# seconds=2.9

say('I will now stack all the blocks into one tower')
order_bottom_to_top = ['red block', 'green block', 'blue block', 'yellow block']
stack_objects_in_order(object_names=order_bottom_to_top)
# verify the stack
all_visible = True
for block_name in order_bottom_to_top:
  if not is_obj_visible(block_name):
    all_visible = False
    say(f'Failed: {block_name} is not visible after stacking')
    break
if all_visible:
  say('Success: all blocks are now stacked into one tower')
