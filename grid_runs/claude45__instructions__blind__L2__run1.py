# model_key=claude45
# model_id=claude-opus-4-5
# provider=anthropic
# condition=instructions
# profile=blind
# task=L2
# run=1
# scene=['red block', 'green block', 'blue block', 'yellow block']
# command=stack all the blocks into one tower.
# generated=2026-08-05T06:22:17
# prompt_chars=12746
# tokens_in=4097 tokens_out=125
# seconds=2.8

say('Stacking all the blocks into one tower')
block_names = parse_obj_name('the blocks', f'objects = {get_obj_names()}')
stack_objects_in_order(object_names=block_names)
# Verify the stack was created successfully
all_visible = all(is_obj_visible(block) for block in block_names)
if all_visible:
  say('Successfully stacked all blocks into one tower')
else:
  say('Some blocks may not have been stacked correctly')
