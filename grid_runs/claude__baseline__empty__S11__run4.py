# model_key=claude
# model_id=claude-opus-4-8
# provider=anthropic
# condition=baseline
# profile=empty
# task=S11
# run=4
# scene=['red block', 'green block', 'blue block', 'red bowl', 'green bowl', 'blue bowl']
# command=put the red block to the left of the rightmost bowl.
# generated=2026-08-05T02:38:27
# prompt_chars=12490
# tokens_in=5275 tokens_out=121
# seconds=2.6

say('Putting the red block to the left of the rightmost bowl')
rightmost_bowl_name = parse_obj_name('the rightmost bowl', f'objects = {get_obj_names()}')
target_pos = parse_position(f'a point 10cm to the left of the {rightmost_bowl_name}')
put_first_on_second('red block', target_pos)
