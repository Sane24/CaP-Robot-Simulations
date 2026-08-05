# model_key=claude45
# model_id=claude-opus-4-5
# provider=anthropic
# condition=predefined_primitives
# profile=blind
# task=L5
# run=3
# scene=['red block', 'green block', 'blue block', 'yellow block']
# command=put the blocks on different corners clockwise starting at the top right corner.
# generated=2026-08-05T07:14:22
# prompt_chars=15340
# tokens_in=4917 tokens_out=224
# seconds=4.1

confirm_before('put the blocks on different corners clockwise starting at the top right corner')
block_names = parse_obj_name('the blocks', f'objects = {get_obj_names()}')
corners = ['top right corner', 'bottom right corner', 'bottom left corner', 'top left corner']
for i, (block_name, corner) in enumerate(zip(block_names, corners)):
    say_progress(i + 1, len(block_names), f'placing the {block_name} on the {corner}')
    corner_pos = parse_position(corner)
    put_first_on_second(block_name, corner_pos)
    say_verified(lambda b=block_name, c=corner_pos: is_at(b, c),
                 f'The {block_name} is on the {corner}.',
                 f'The {block_name} did not end up on the {corner}.')
