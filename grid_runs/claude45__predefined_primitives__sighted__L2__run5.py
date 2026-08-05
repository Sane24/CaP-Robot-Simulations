# model_key=claude45
# model_id=claude-opus-4-5
# provider=anthropic
# condition=predefined_primitives
# profile=sighted
# task=L2
# run=5
# scene=['red block', 'green block', 'blue block', 'yellow block']
# command=stack all the blocks into one tower.
# generated=2026-08-05T07:18:49
# prompt_chars=15299
# tokens_in=4911 tokens_out=142
# seconds=2.9

confirm_before('stack all the blocks into one tower')
block_names = parse_obj_name('the blocks', f'objects = {get_obj_names()}')
stack_objects_in_order(object_names=block_names)
for i, block_name in enumerate(block_names[1:], start=1):
    say_verified(lambda b=block_name, below=block_names[i-1]: is_placed(b, below),
                 f'The {block_name} is stacked correctly.',
                 f'The {block_name} did not stack correctly.')
