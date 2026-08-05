# model_key=claude45
# model_id=claude-opus-4-5
# provider=anthropic
# condition=predefined_primitives
# profile=sighted_assist
# task=S7
# run=1
# scene=['red block', 'green block', 'blue block', 'yellow block']
# command=move the sky-colored block in between the red block and the second block from the left.
# generated=2026-08-05T07:34:57
# prompt_chars=15393
# tokens_in=4930 tokens_out=167
# seconds=10.7

second_from_left_block = parse_obj_name('the second block from the left', f'objects = {get_obj_names()}')
target_pos = parse_position(f'a point in the middle between the red block and the {second_from_left_block}')
confirm_before(f'move the blue block in between the red block and the {second_from_left_block}')
put_first_on_second('blue block', target_pos)
say_verified(lambda: is_at('blue block', target_pos),
             'Done, the blue block is now between the red block and the second block from the left.',
             'The blue block did not end up in the expected position.')
