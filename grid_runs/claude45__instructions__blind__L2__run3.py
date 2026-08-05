# model_key=claude45
# model_id=claude-opus-4-5
# provider=anthropic
# condition=instructions
# profile=blind
# task=L2
# run=3
# scene=['red block', 'green block', 'blue block', 'yellow block']
# command=stack all the blocks into one tower.
# generated=2026-08-05T06:22:29
# prompt_chars=12746
# tokens_in=4097 tokens_out=175
# seconds=5.3

say('Stacking all the blocks into one tower')
block_names = parse_obj_name('the blocks', f'objects = {get_obj_names()}')
stack_objects_in_order(object_names=block_names)
# Verify the stack was successful
final_positions = [get_obj_pos(block) for block in block_names]
all_same_xy = all(np.allclose(final_positions[0][:2], pos[:2], atol=0.02) for pos in final_positions)
if all_same_xy:
  say('Success - all blocks are now stacked in one tower')
else:
  say('The stacking may not have fully succeeded - some blocks might not be aligned')
