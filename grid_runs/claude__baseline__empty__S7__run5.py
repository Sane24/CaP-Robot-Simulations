# model_key=claude
# model_id=claude-opus-4-8
# provider=anthropic
# condition=baseline
# profile=empty
# task=S7
# run=5
# scene=['red block', 'green block', 'blue block', 'yellow block']
# command=move the sky-colored block in between the red block and the second block from the left.
# generated=2026-08-05T02:38:01
# prompt_chars=12502
# tokens_in=5264 tokens_out=118
# seconds=2.6

second_block_name = parse_obj_name('the second block from the left', f'objects = {get_obj_names()}')
target_pos = parse_position(f'a point in the middle between the red block and the {second_block_name}')
say(f'Ok - putting the blue block between the red block and the {second_block_name}')
put_first_on_second('blue block', target_pos)
