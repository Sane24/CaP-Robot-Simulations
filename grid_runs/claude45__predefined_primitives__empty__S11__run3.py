# model_key=claude45
# model_id=claude-opus-4-5
# provider=anthropic
# condition=predefined_primitives
# profile=empty
# task=S11
# run=3
# scene=['red block', 'green block', 'blue block', 'red bowl', 'green bowl', 'blue bowl']
# command=put the red block to the left of the rightmost bowl.
# generated=2026-08-05T06:59:51
# prompt_chars=15303
# tokens_in=4916 tokens_out=163
# seconds=3.2

left_pos = parse_position('a point 10cm to the left of the rightmost bowl')
rightmost_bowl_name = parse_obj_name('the rightmost bowl', f'objects = {get_obj_names()}')
confirm_before(f'put the red block to the left of the {rightmost_bowl_name}')
put_first_on_second('red block', left_pos)
say_verified(lambda: is_at('red block', left_pos),
             f'The red block is now to the left of the {rightmost_bowl_name}.',
             f'The red block did not end up to the left of the {rightmost_bowl_name}.')
