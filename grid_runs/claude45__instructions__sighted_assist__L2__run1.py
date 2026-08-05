# model_key=claude45
# model_id=claude-opus-4-5
# provider=anthropic
# condition=instructions
# profile=sighted_assist
# task=L2
# run=1
# scene=['red block', 'green block', 'blue block', 'yellow block']
# command=stack all the blocks into one tower.
# generated=2026-08-05T06:53:44
# prompt_chars=12791
# tokens_in=4106 tokens_out=200
# seconds=3.9

say('Ok - stacking all the blocks into one tower')
block_names = parse_obj_name('the blocks', f'objects = {get_obj_names()}')
stack_objects_in_order(object_names=block_names)
say('Checking if the stack was successful')
# Verify the stack by checking positions
positions_correct = True
for i in range(1, len(block_names)):
    lower_pos = get_obj_pos(block_names[i-1])
    upper_pos = get_obj_pos(block_names[i])
    if upper_pos[2] <= lower_pos[2]:
        positions_correct = False
        break
if positions_correct:
    say('Success - all blocks are stacked in a tower')
else:
    say('The stacking did not succeed as expected')
