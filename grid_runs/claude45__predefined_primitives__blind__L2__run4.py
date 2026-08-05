# model_key=claude45
# model_id=claude-opus-4-5
# provider=anthropic
# condition=predefined_primitives
# profile=blind
# task=L2
# run=4
# scene=['red block', 'green block', 'blue block', 'yellow block']
# command=stack all the blocks into one tower.
# generated=2026-08-05T07:10:22
# prompt_chars=15297
# tokens_in=4910 tokens_out=190
# seconds=5.5

confirm_before('stack all the blocks into one tower')
block_names = parse_obj_name('the blocks', f'objects = {get_obj_names()}')
for i, block_name in enumerate(block_names):
    say_progress(i + 1, len(block_names), f'stacking the {block_name}')
    if i == 0:
        # first block stays in place as the base
        continue
    put_first_on_second(block_name, block_names[i - 1])
    say_verified(lambda b=block_name, prev=block_names[i-1]: is_placed(b, prev),
                 f'The {block_name} is stacked.',
                 f'The {block_name} did not stack properly.')
