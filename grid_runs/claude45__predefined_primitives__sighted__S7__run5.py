# model_key=claude45
# model_id=claude-opus-4-5
# provider=anthropic
# condition=predefined_primitives
# profile=sighted
# task=S7
# run=5
# scene=['red block', 'green block', 'blue block', 'yellow block']
# command=move the sky-colored block in between the red block and the second block from the left.
# generated=2026-08-05T07:17:28
# prompt_chars=15350
# tokens_in=4922 tokens_out=165
# seconds=4.8

second_block_from_left = parse_obj_name('the second block from the left', f'objects = {get_obj_names()}')
target_pos = parse_position(f'a point in the middle between the red block and the {second_block_from_left}')
confirm_before(f'move the blue block in between the red block and the {second_block_from_left}')
put_first_on_second('blue block', target_pos)
say_verified(lambda: is_at('blue block', target_pos),
             'The blue block is now between the red block and the second block from the left.',
             'The blue block did not end up in the target position.')
