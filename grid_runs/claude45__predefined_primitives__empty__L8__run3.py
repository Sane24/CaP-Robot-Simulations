# model_key=claude45
# model_id=claude-opus-4-5
# provider=anthropic
# condition=predefined_primitives
# profile=empty
# task=L8
# run=3
# scene=['red block', 'green block', 'blue block', 'red bowl', 'green bowl', 'blue bowl']
# command=place the blocks in bowls with non-matching colors.
# generated=2026-08-05T07:03:20
# prompt_chars=15302
# tokens_in=4915 tokens_out=288
# seconds=6.0

confirm_before('place the blocks in bowls with non-matching colors')
block_names = parse_obj_name('the blocks', f'objects = {get_obj_names()}')
bowl_names = parse_obj_name('the bowls', f'objects = {get_obj_names()}')
for i, block_name in enumerate(block_names):
    say_progress(i + 1, len(block_names), f'placing the {block_name} in a non-matching bowl')
    block_color = block_name.split()[0]
    non_matching_bowls = [b for b in bowl_names if not b.startswith(block_color)]
    if non_matching_bowls:
        target_bowl = non_matching_bowls[0]
        put_first_on_second(block_name, target_bowl)
        say_verified(lambda b=block_name, t=target_bowl: is_in_bowl(b, t),
                     f'The {block_name} is in the {target_bowl}.',
                     f'The {block_name} did not end up in the {target_bowl}.')
        bowl_names.remove(target_bowl)
