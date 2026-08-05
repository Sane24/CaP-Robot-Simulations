# model_key=claude
# model_id=claude-opus-4-8
# provider=anthropic
# condition=baseline
# profile=blind
# task=S7
# run=2
# scene=['red block', 'green block', 'blue block', 'yellow block']
# command=move the sky-colored block in between the red block and the second block from the left.
# generated=2026-08-05T02:41:54
# prompt_chars=12535
# tokens_in=5274 tokens_out=124
# seconds=3.5

second_left_block_name = parse_obj_name('the second block from the left', f'objects = {get_obj_names()}')
target_pos = parse_position(f'a point in the middle between the red block and the {second_left_block_name}')
say(f'Ok - putting the blue block between the red block and the {second_left_block_name}')
put_first_on_second('blue block', target_pos)
