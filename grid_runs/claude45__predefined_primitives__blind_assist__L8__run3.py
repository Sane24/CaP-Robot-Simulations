# model_key=claude45
# model_id=claude-opus-4-5
# provider=anthropic
# condition=predefined_primitives
# profile=blind_assist
# task=L8
# run=3
# scene=['red block', 'green block', 'blue block', 'red bowl', 'green bowl', 'blue bowl']
# command=place the blocks in bowls with non-matching colors.
# generated=2026-08-05T07:29:55
# prompt_chars=15378
# tokens_in=4932 tokens_out=241
# seconds=12.1

confirm_before('place the blocks in bowls with non-matching colors')
blocks = ['red block', 'green block', 'blue block']
bowls = ['red bowl', 'green bowl', 'blue bowl']
for i, block in enumerate(blocks):
    block_color = block.split()[0]
    non_matching_bowls = [b for b in bowls if not b.startswith(block_color)]
    target_bowl = non_matching_bowls[0]
    bowls.remove(target_bowl)
    say_progress(i + 1, len(blocks), f'placing the {block} in the {target_bowl}')
    put_first_on_second(block, target_bowl)
    say_verified(lambda b=block, bowl=target_bowl: is_in_bowl(b, bowl),
                 f'The {block} is in the {target_bowl}.',
                 f'The {block} did not end up in the {target_bowl}.')
