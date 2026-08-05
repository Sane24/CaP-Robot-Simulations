# model_key=claude
# model_id=claude-opus-4-8
# provider=anthropic
# condition=baseline
# profile=blind_assist
# task=S7
# run=1
# scene=['red block', 'green block', 'blue block', 'yellow block']
# command=move the sky-colored block in between the red block and the second block from the left.
# generated=2026-08-05T02:50:27
# prompt_chars=12578
# tokens_in=5286 tokens_out=130
# seconds=2.7

second_from_left_block_name = parse_obj_name('the second block from the left', f'objects = {get_obj_names()}')
say(f'Got it - putting the blue block between the red block and the {second_from_left_block_name}')
target_pos = parse_position(f'a point in the middle between the red block and the {second_from_left_block_name}')
put_first_on_second('blue block', target_pos)
