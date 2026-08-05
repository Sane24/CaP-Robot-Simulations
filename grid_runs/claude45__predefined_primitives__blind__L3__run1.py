# model_key=claude45
# model_id=claude-opus-4-5
# provider=anthropic
# condition=predefined_primitives
# profile=blind
# task=L3
# run=1
# scene=['red block', 'green block', 'blue block', 'yellow block']
# command=put the blocks in a horizontal line near the top.
# generated=2026-08-05T07:10:30
# prompt_chars=15310
# tokens_in=4913 tokens_out=217
# seconds=3.9

say('Ok - putting the blocks in a horizontal line near the top')
block_names = parse_obj_name('the blocks', f'objects = {get_obj_names()}')
line_pts = parse_position(f'a 30cm horizontal line near the top with {len(block_names)} points')
confirm_before('put the blocks in a horizontal line near the top')
for i, (block_name, pt) in enumerate(zip(block_names, line_pts)):
    say_progress(i + 1, len(block_names), f'placing the {block_name}')
    put_first_on_second(block_name, pt)
    say_verified(lambda b=block_name, p=pt: is_at(b, p),
                 f'The {block_name} is in position.',
                 f'The {block_name} did not end up in the expected position.')
