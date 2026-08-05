# model_key=claude45
# model_id=claude-opus-4-5
# provider=anthropic
# condition=predefined_primitives
# profile=sighted_assist
# task=S7
# run=2
# scene=['red block', 'green block', 'blue block', 'yellow block']
# command=move the sky-colored block in between the red block and the second block from the left.
# generated=2026-08-05T07:35:04
# prompt_chars=15393
# tokens_in=4930 tokens_out=101
# seconds=7.4

say('Ok - moving the blue block between the red block and the second block from the left')
second_from_left = parse_obj_name('the second block from the left', f'objects = {get_obj_names()}')
target_pos = parse_position(f'a point in the middle between the red block and the {second_from_left}')
put_first_on_second('blue block', target_pos)
