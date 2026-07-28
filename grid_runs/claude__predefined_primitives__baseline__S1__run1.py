# model_key=claude
# model_id=claude-opus-4-5
# provider=anthropic
# condition=predefined_primitives
# profile=baseline
# task=S1
# run=1
# scene=['red block', 'green block']
# command=put the red block on the green block.
# generated=2026-07-23T10:55:26
# prompt_chars=14586
# tokens_in=4693 tokens_out=81
# seconds=3.2

confirm_before('put the red block on the green block')
put_first_on_second('red block', 'green block')
say_verified(lambda: is_placed('red block', 'green block'),
             'Done, the red block is on the green block.',
             'The red block did not end up on the green block.')
