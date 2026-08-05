# model_key=claude45
# model_id=claude-opus-4-5
# provider=anthropic
# condition=predefined_primitives
# profile=sighted
# task=S2
# run=4
# scene=['cube']
# command=lift the cube above the table.
# generated=2026-08-05T07:15:21
# prompt_chars=15243
# tokens_in=4894 tokens_out=52
# seconds=9.1

confirm_before('lift the cube above the table')
lift('cube')
say_verified(lambda: was_lifted('cube'),
             'The cube was lifted above the table.',
             'The cube was not lifted.')
