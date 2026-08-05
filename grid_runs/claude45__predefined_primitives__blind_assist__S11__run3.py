# model_key=claude45
# model_id=claude-opus-4-5
# provider=anthropic
# condition=predefined_primitives
# profile=blind_assist
# task=S11
# run=3
# scene=['red block', 'green block', 'blue block', 'red bowl', 'green bowl', 'blue bowl']
# command=put the red block to the left of the rightmost bowl.
# generated=2026-08-05T07:25:28
# prompt_chars=15379
# tokens_in=4933 tokens_out=95
# seconds=2.9

say('Putting the red block to the left of the rightmost bowl')
rightmost_bowl_name = parse_obj_name('rightmost bowl', f'objects = {get_obj_names()}')
target_pos = parse_position(f'a point 10cm to the left of the {rightmost_bowl_name}')
put_first_on_second('red block', target_pos)
