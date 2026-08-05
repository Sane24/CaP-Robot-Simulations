# model_key=claude45
# model_id=claude-opus-4-5
# provider=anthropic
# condition=instructions
# profile=sighted
# task=S7
# run=3
# scene=['red block', 'green block', 'blue block', 'yellow block']
# command=move the sky-colored block in between the red block and the second block from the left.
# generated=2026-08-05T06:29:14
# prompt_chars=12799
# tokens_in=4109 tokens_out=108
# seconds=2.3

second_from_left_block = parse_obj_name('second block from the left', f'objects = {get_obj_names()}')
say(f'Moving the blue block between the red block and the {second_from_left_block}')
target_pos = parse_position(f'a point in the middle between the red block and the {second_from_left_block}')
put_first_on_second('blue block', target_pos)
