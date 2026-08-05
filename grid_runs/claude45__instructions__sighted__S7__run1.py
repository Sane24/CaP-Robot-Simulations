# model_key=claude45
# model_id=claude-opus-4-5
# provider=anthropic
# condition=instructions
# profile=sighted
# task=S7
# run=1
# scene=['red block', 'green block', 'blue block', 'yellow block']
# command=move the sky-colored block in between the red block and the second block from the left.
# generated=2026-08-05T06:29:09
# prompt_chars=12799
# tokens_in=4109 tokens_out=100
# seconds=3.3

say('Ok - moving the blue block between the red block and the second block from the left')
second_from_left = parse_obj_name('second block from the left', f'objects = {get_obj_names()}')
target_pos = parse_position(f'a point in the middle between the red block and the {second_from_left}')
put_first_on_second('blue block', target_pos)
