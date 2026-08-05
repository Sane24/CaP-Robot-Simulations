# model_key=claude45
# model_id=claude-opus-4-5
# provider=anthropic
# condition=predefined_primitives
# profile=blind
# task=S7
# run=2
# scene=['red block', 'green block', 'blue block', 'yellow block']
# command=move the sky-colored block in between the red block and the second block from the left.
# generated=2026-08-05T07:08:18
# prompt_chars=15348
# tokens_in=4921 tokens_out=166
# seconds=5.0

second_from_left_block = parse_obj_name('second block from the left', f'objects = {get_obj_names()}')
confirm_before(f'move the blue block in between the red block and the {second_from_left_block}')
target_pos = parse_position(f'a point in the middle between the red block and the {second_from_left_block}')
put_first_on_second('blue block', target_pos)
say_verified(lambda: is_at('blue block', target_pos),
             'Done, the blue block is now between the red block and the second block from the left.',
             'The blue block did not end up in the expected position.')
