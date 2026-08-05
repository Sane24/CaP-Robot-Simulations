# model_key=claude45
# model_id=claude-opus-4-5
# provider=anthropic
# condition=predefined_primitives
# profile=sighted
# task=S11
# run=1
# scene=['red block', 'green block', 'blue block', 'red bowl', 'green bowl', 'blue bowl']
# command=put the red block to the left of the rightmost bowl.
# generated=2026-08-05T07:17:59
# prompt_chars=15338
# tokens_in=4926 tokens_out=171
# seconds=3.3

rightmost_bowl_name = parse_obj_name('the rightmost bowl', f'objects = {get_obj_names()}')
target_pos = parse_position(f'a point 10cm to the left of the {rightmost_bowl_name}')
confirm_before(f'put the red block to the left of the {rightmost_bowl_name}')
put_first_on_second('red block', target_pos)
say_verified(lambda: is_at('red block', target_pos),
             f'Done, the red block is to the left of the {rightmost_bowl_name}.',
             f'The red block did not end up to the left of the {rightmost_bowl_name}.')
