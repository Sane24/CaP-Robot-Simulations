# model_key=claude
# model_id=claude-opus-4-5
# provider=anthropic
# condition=predefined_primitives
# profile=sighted_assist
# task=S1
# run=2
# scene=['red block', 'green block']
# command=put the red block on the green block.
# generated=2026-07-23T10:56:28
# prompt_chars=14664
# tokens_in=4711 tokens_out=81
# seconds=2.6

confirm_before('put the red block on the green block')
put_first_on_second('red block', 'green block')
say_verified(lambda: is_placed('red block', 'green block'),
             'Done, the red block is on the green block.',
             'The red block did not end up on the green block.')
