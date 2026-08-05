# model_key=claude45
# model_id=claude-opus-4-5
# provider=anthropic
# condition=predefined_primitives
# profile=empty
# task=S1
# run=4
# scene=['red block', 'green block']
# command=put the red block on the green block.
# generated=2026-08-05T06:56:54
# prompt_chars=15235
# tokens_in=4892 tokens_out=81
# seconds=2.1

confirm_before('put the red block on the green block')
put_first_on_second('red block', 'green block')
say_verified(lambda: is_placed('red block', 'green block'),
             'Done, the red block is on the green block.',
             'The red block did not end up on the green block.')
