# model_key=claude45
# model_id=claude-opus-4-5
# provider=anthropic
# condition=instructions
# profile=blind
# task=L2
# run=5
# scene=['red block', 'green block', 'blue block', 'yellow block']
# command=stack all the blocks into one tower.
# generated=2026-08-05T06:22:35
# prompt_chars=12746
# tokens_in=4097 tokens_out=140
# seconds=3.1

say('Stacking all the blocks into one tower')
block_names = parse_obj_name('the blocks', f'objects = {get_obj_names()}')
stack_objects_in_order(object_names=block_names)
# Verify the stack was successful
for i, block_name in enumerate(block_names):
    if is_obj_visible(block_name):
        say(f'{block_name} is in position')
    else:
        say(f'Could not verify {block_name} position')
say('Finished stacking all blocks into a tower')
