# model_key=claude45
# model_id=claude-opus-4-5
# provider=anthropic
# condition=predefined_primitives
# profile=blind
# task=L6
# run=3
# scene=['red block', 'green block', 'blue block', 'yellow block']
# command=arrange the blocks in a square around the middle.
# generated=2026-08-05T07:11:52
# prompt_chars=15310
# tokens_in=4912 tokens_out=201
# seconds=4.3

block_names = parse_obj_name('the blocks', f'objects = {get_obj_names()}')
confirm_before('arrange the blocks in a square around the middle')
square_pts = parse_position(f'a square with size 15cm around the middle with {len(block_names)} points')
for i, (block_name, pt) in enumerate(zip(block_names, square_pts)):
    say_progress(i + 1, len(block_names), f'placing the {block_name}')
    put_first_on_second(block_name, pt)
    say_verified(lambda b=block_name, p=pt: is_at(b, p),
                 f'The {block_name} is in position.',
                 f'The {block_name} did not end up in the correct position.')
