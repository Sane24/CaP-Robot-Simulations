# model_key=claude45
# model_id=claude-opus-4-5
# provider=anthropic
# condition=predefined_primitives
# profile=empty
# task=L9
# run=2
# scene=['red block', 'green block', 'blue block', 'yellow block']
# command=arrange the blocks in a square around the middle. then, make the square bigger.
# generated=2026-08-05T07:03:59
# prompt_chars=15307
# tokens_in=4910 tokens_out=354
# seconds=12.5

block_names = parse_obj_name('the blocks', f'objects = {get_obj_names()}')
square_pts = parse_position(f'a square with size 10cm around the middle with {len(block_names)} points')
confirm_before('arrange the blocks in a square around the middle')
for i, (block_name, pt) in enumerate(zip(block_names, square_pts)):
    say_progress(i + 1, len(block_names), f'placing {block_name}')
    put_first_on_second(block_name, pt)
    say_verified(lambda b=block_name, p=pt: is_at(b, p),
                 f'{block_name} is in position.',
                 f'{block_name} did not end up in position.')

square_pts = transform_shape_pts('scale it by 1.5x', shape_pts=square_pts)
confirm_before('make the square bigger')
for i, (block_name, pt) in enumerate(zip(block_names, square_pts)):
    say_progress(i + 1, len(block_names), f'moving {block_name} outward')
    put_first_on_second(block_name, pt)
    say_verified(lambda b=block_name, p=pt: is_at(b, p),
                 f'{block_name} is in position.',
                 f'{block_name} did not end up in position.')
