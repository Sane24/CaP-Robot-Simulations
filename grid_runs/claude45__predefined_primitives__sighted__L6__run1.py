# model_key=claude45
# model_id=claude-opus-4-5
# provider=anthropic
# condition=predefined_primitives
# profile=sighted
# task=L6
# run=1
# scene=['red block', 'green block', 'blue block', 'yellow block']
# command=arrange the blocks in a square around the middle.
# generated=2026-08-05T07:20:06
# prompt_chars=15312
# tokens_in=4913 tokens_out=199
# seconds=4.0

block_names = parse_obj_name('the blocks', f'objects = {get_obj_names()}')
square_pts = parse_position(f'a square with size 10cm around the middle with {len(block_names)} points')
confirm_before('arrange the blocks in a square around the middle')
for i, (block_name, pt) in enumerate(zip(block_names, square_pts)):
    say_progress(i + 1, len(block_names), f'placing the {block_name}')
    put_first_on_second(block_name, pt)
    say_verified(lambda b=block_name, p=pt: is_at(b, p),
                 f'The {block_name} is in position.',
                 f'The {block_name} did not end up in position.')
