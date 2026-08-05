# model_key=claude45
# model_id=claude-opus-4-5
# provider=anthropic
# condition=predefined_primitives
# profile=blind
# task=L7
# run=1
# scene=['red block', 'green block', 'blue block', 'red bowl', 'green bowl', 'blue bowl']
# command=put the blocks in a vertical line 20cm long and 10cm below the blue bowl.
# generated=2026-08-05T07:12:08
# prompt_chars=15357
# tokens_in=4932 tokens_out=239
# seconds=6.1

say('Ok - putting the blocks in a vertical line 20cm long and 10cm below the blue bowl')
block_names = parse_obj_name('the blocks', f'objects = {get_obj_names()}')
line_pts = parse_position(f'a 20cm vertical line 10cm below the blue bowl with {len(block_names)} points')
confirm_before('put the blocks in a vertical line 20cm long and 10cm below the blue bowl')
for i, (block_name, pt) in enumerate(zip(block_names, line_pts)):
    say_progress(i + 1, len(block_names), f'placing the {block_name}')
    put_first_on_second(block_name, pt)
    say_verified(lambda b=block_name, p=pt: is_at(b, p),
                 f'The {block_name} is in position.',
                 f'The {block_name} did not end up in the correct position.')
