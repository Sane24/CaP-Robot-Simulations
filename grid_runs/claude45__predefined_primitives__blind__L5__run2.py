# model_key=claude45
# model_id=claude-opus-4-5
# provider=anthropic
# condition=predefined_primitives
# profile=blind
# task=L5
# run=2
# scene=['red block', 'green block', 'blue block', 'yellow block']
# command=put the blocks on different corners clockwise starting at the top right corner.
# generated=2026-08-05T07:14:18
# prompt_chars=15340
# tokens_in=4917 tokens_out=256
# seconds=4.9

say('Ok - putting the blocks on different corners clockwise starting at the top right corner')
confirm_before('put the blocks on different corners clockwise starting at the top right corner')
block_names = parse_obj_name('the blocks', f'objects = {get_obj_names()}')
corners = [parse_position('top right corner'), parse_position('bottom right corner'), parse_position('bottom left corner'), parse_position('top left corner')]
for i, (block_name, pos) in enumerate(zip(block_names, corners)):
    say_progress(i + 1, len(block_names), f'placing the {block_name} on the {get_corner_name(pos)}')
    put_first_on_second(block_name, pos)
    say_verified(lambda b=block_name, p=pos: is_at(b, p),
                 f'The {block_name} is on the {get_corner_name(pos)}.',
                 f'The {block_name} did not end up on the {get_corner_name(pos)}.')
