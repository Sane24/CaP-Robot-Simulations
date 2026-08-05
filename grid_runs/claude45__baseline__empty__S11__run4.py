# model_key=claude45
# model_id=claude-opus-4-5
# provider=anthropic
# condition=baseline
# profile=empty
# task=S11
# run=4
# scene=['red block', 'green block', 'blue block', 'red bowl', 'green bowl', 'blue bowl']
# command=put the red block to the left of the rightmost bowl.
# generated=2026-08-05T03:32:37
# prompt_chars=12490
# tokens_in=4046 tokens_out=103
# seconds=2.0

rightmost_bowl_name = parse_obj_name('the rightmost bowl', f'objects = {get_obj_names()}')
target_pos = parse_position(f'a point 10cm to the left of the {rightmost_bowl_name}')
say(f'Putting the red block to the left of the {rightmost_bowl_name}')
put_first_on_second('red block', target_pos)
