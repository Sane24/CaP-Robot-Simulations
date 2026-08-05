# model_key=claude45
# model_id=claude-opus-4-5
# provider=anthropic
# condition=predefined_primitives
# profile=blind
# task=L2
# run=1
# scene=['red block', 'green block', 'blue block', 'yellow block']
# command=stack all the blocks into one tower.
# generated=2026-08-05T07:10:05
# prompt_chars=15297
# tokens_in=4910 tokens_out=199
# seconds=5.8

confirm_before('stack all the blocks into one tower')
block_names = parse_obj_name('the blocks', f'objects = {get_obj_names()}')
for i, block_name in enumerate(block_names):
    say_progress(i + 1, len(block_names), f'stacking the {block_name}')
    if i == 0:
        # first block is the base, no need to move
        continue
    put_first_on_second(block_name, block_names[i - 1])
    say_verified(lambda b=block_name, base=block_names[i-1]: is_placed(b, base),
                 f'The {block_name} is stacked.',
                 f'The {block_name} did not stack properly.')
pause_for_verification()
