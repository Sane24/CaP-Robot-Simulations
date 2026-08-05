# model_key=claude45
# model_id=claude-opus-4-5
# provider=anthropic
# condition=instructions
# profile=sighted_assist
# task=L2
# run=3
# scene=['red block', 'green block', 'blue block', 'yellow block']
# command=stack all the blocks into one tower.
# generated=2026-08-05T06:53:55
# prompt_chars=12791
# tokens_in=4106 tokens_out=213
# seconds=6.1

say('Ok - stacking all the blocks into one tower')
block_names = parse_obj_name('the blocks', f'objects = {get_obj_names()}')
stack_objects_in_order(object_names=block_names)
say('Checking if the stack was successful')
# Verify the stack by checking positions
positions_verified = True
for i in range(1, len(block_names)):
    bottom_pos = get_obj_pos(block_names[i-1])
    top_pos = get_obj_pos(block_names[i])
    if top_pos[2] <= bottom_pos[2]:
        positions_verified = False
        say(f'Stack failed: {block_names[i]} is not above {block_names[i-1]}')
        break
if positions_verified:
    say('Success - all blocks are stacked into one tower')
