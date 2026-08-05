# model_key=claude45
# model_id=claude-opus-4-5
# provider=anthropic
# condition=instructions
# profile=blind_assist
# task=L5
# run=1
# scene=['red block', 'green block', 'blue block', 'yellow block']
# command=put the blocks on different corners clockwise starting at the top right corner.
# generated=2026-08-05T06:48:19
# prompt_chars=12832
# tokens_in=4112 tokens_out=234
# seconds=5.3

say('Placing blocks on corners clockwise starting from top right')
corners = parse_position('the corners clockwise starting from top right')
block_names = parse_obj_name('the blocks', f'objects = {get_obj_names()}')
for block_name, corner_pos in zip(block_names, corners):
    put_first_on_second(block_name, corner_pos)
    actual_pos = get_obj_pos(block_name)
    expected_corner = get_corner_name(corner_pos)
    actual_corner = get_corner_name(actual_pos)
    if np.linalg.norm(np.array(actual_pos) - np.array(corner_pos)) < 0.05:
        say(f'Successfully placed {block_name} on the {expected_corner}')
    else:
        say(f'Failed to place {block_name} on the {expected_corner}, it ended up near the {actual_corner}')
