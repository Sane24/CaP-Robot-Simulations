# model_key=claude45
# model_id=claude-opus-4-5
# provider=anthropic
# condition=predefined_primitives
# profile=sighted
# task=L8
# run=5
# scene=['red block', 'green block', 'blue block', 'red bowl', 'green bowl', 'blue bowl']
# command=place the blocks in bowls with non-matching colors.
# generated=2026-08-05T07:21:02
# prompt_chars=15337
# tokens_in=4925 tokens_out=214
# seconds=3.9

confirm_before('place the blocks in bowls with non-matching colors')
blocks = ['red block', 'green block', 'blue block']
bowls = ['red bowl', 'green bowl', 'blue bowl']
# Assign each block to a bowl with a different color
assignments = [('red block', 'green bowl'), ('green block', 'blue bowl'), ('blue block', 'red bowl')]
for i, (block, bowl) in enumerate(assignments):
    say_progress(i + 1, len(assignments), f'placing the {block} in the {bowl}')
    put_first_on_second(block, bowl)
    say_verified(lambda b=block, w=bowl: is_in_bowl(b, w),
                 f'The {block} is in the {bowl}.',
                 f'The {block} did not end up in the {bowl}.')
