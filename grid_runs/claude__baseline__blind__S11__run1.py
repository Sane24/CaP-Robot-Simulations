# model_key=claude
# model_id=claude-opus-4-8
# provider=anthropic
# condition=baseline
# profile=blind
# task=S11
# run=1
# scene=['red block', 'green block', 'blue block', 'red bowl', 'green bowl', 'blue bowl']
# command=put the red block to the left of the rightmost bowl.
# generated=2026-08-05T02:42:22
# prompt_chars=12523
# tokens_in=5285 tokens_out=131
# seconds=2.3

rightmost_bowl_name = parse_obj_name('the rightmost bowl', f'objects = {get_obj_names()}')
target_pos = parse_position(f'a point 10cm to the left of the {rightmost_bowl_name}')
say(f'Ok - putting the red block to the left of the {rightmost_bowl_name}')
put_first_on_second('red block', target_pos)
