# model_key=claude45
# model_id=claude-opus-4-5
# provider=anthropic
# condition=predefined_primitives
# profile=empty
# task=L5
# run=4
# scene=['red block', 'green block', 'blue block', 'yellow block']
# command=put the blocks on different corners clockwise starting at the top right corner.
# generated=2026-08-05T07:05:09
# prompt_chars=15307
# tokens_in=4908 tokens_out=233
# seconds=4.1

corners = ['top right corner', 'bottom right corner', 'bottom left corner', 'top left corner']
corner_positions = [parse_position(c) for c in corners]
block_names = parse_obj_name('the blocks', f'objects = {get_obj_names()}')
confirm_before('put the blocks on different corners clockwise starting at the top right corner')
for i, (block_name, pos) in enumerate(zip(block_names, corner_positions)):
    say_progress(i + 1, len(block_names), f'placing the {block_name} on the {corners[i]}')
    put_first_on_second(block_name, pos)
    say_verified(lambda b=block_name, p=pos: is_at(b, p),
                 f'The {block_name} is on the {corners[i]}.',
                 f'The {block_name} did not end up on the {corners[i]}.')
