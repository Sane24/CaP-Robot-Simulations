# model_key=claude45
# model_id=claude-opus-4-5
# provider=anthropic
# condition=predefined_primitives
# profile=blind
# task=S2
# run=4
# scene=['cube']
# command=lift the cube above the table.
# generated=2026-08-05T07:06:18
# prompt_chars=15241
# tokens_in=4893 tokens_out=61
# seconds=9.6

confirm_before('lift the cube above the table')
lift('cube')
say_verified(lambda: was_lifted('cube'),
             'The cube has been lifted above the table.',
             'The cube was not lifted successfully.')
pause_for_verification()
