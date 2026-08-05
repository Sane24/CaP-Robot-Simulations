# model_key=claude
# model_id=claude-opus-4-8
# provider=anthropic
# condition=baseline
# profile=sighted
# task=S7
# run=4
# scene=['red block', 'green block', 'blue block', 'yellow block']
# command=move the sky-colored block in between the red block and the second block from the left.
# generated=2026-08-05T02:46:09
# prompt_chars=12537
# tokens_in=5275 tokens_out=115
# seconds=2.8

second_block_name = parse_obj_name('the second block from the left', f'objects = {get_obj_names()}')
target_pos = parse_position(f'a point in the middle between the red block and the {second_block_name}')
say('Sure - moving the blue block in between the red block and the second block from the left')
put_first_on_second('blue block', target_pos)
