# model_key=claude45
# model_id=claude-opus-4-5
# provider=anthropic
# condition=predefined_primitives
# profile=blind_assist
# task=L5
# run=1
# scene=['red block', 'green block', 'blue block', 'yellow block']
# command=put the blocks on different corners clockwise starting at the top right corner.
# generated=2026-08-05T07:32:03
# prompt_chars=15383
# tokens_in=4925 tokens_out=271
# seconds=11.4

say('Ok - putting the blocks on different corners clockwise starting at the top right corner')
block_names = parse_obj_name('the blocks', f'objects = {get_obj_names()}')
corners = ['top right corner', 'bottom right corner', 'bottom left corner', 'top left corner']
for i, block_name in enumerate(block_names):
    corner_pos = parse_position(corners[i % len(corners)])
    confirm_before(f'put the {block_name} on the {corners[i % len(corners)]}')
    say_progress(i + 1, len(block_names), f'placing the {block_name} on the {corners[i % len(corners)]}')
    put_first_on_second(block_name, corner_pos)
    say_verified(lambda b=block_name, c=corner_pos: is_at(b, c),
                 f'The {block_name} is on the {corners[i % len(corners)]}.',
                 f'The {block_name} did not end up on the {corners[i % len(corners)]}.')
