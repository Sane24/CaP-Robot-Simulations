# model_key=claude45
# model_id=claude-opus-4-5
# provider=anthropic
# condition=instructions
# profile=blind
# task=L2
# run=2
# scene=['red block', 'green block', 'blue block', 'yellow block']
# command=stack all the blocks into one tower.
# generated=2026-08-05T06:22:24
# prompt_chars=12746
# tokens_in=4097 tokens_out=129
# seconds=7.0

say('Stacking all the blocks into one tower')
block_names = parse_obj_name('the blocks', f'objects = {get_obj_names()}')
stack_objects_in_order(object_names=block_names)
# verify the stack
for i, block_name in enumerate(block_names):
    if is_obj_visible(block_name):
        say(f'Verified: {block_name} is in position')
    else:
        say(f'Could not verify position of {block_name}')
