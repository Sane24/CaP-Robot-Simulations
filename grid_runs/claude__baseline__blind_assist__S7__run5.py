# model_key=claude
# model_id=claude-opus-4-8
# provider=anthropic
# condition=baseline
# profile=blind_assist
# task=S7
# run=5
# scene=['red block', 'green block', 'blue block', 'yellow block']
# command=move the sky-colored block in between the red block and the second block from the left.
# generated=2026-08-05T02:50:37
# prompt_chars=12578
# tokens_in=5286 tokens_out=130
# seconds=2.8

second_block_from_left_name = parse_obj_name('the second block from the left', f'objects = {get_obj_names()}')
say(f'Ok - putting the blue block between the red block and the {second_block_from_left_name}')
target_pos = parse_position(f'a point in the middle between the red block and the {second_block_from_left_name}')
put_first_on_second('blue block', target_pos)
