# model_key=claude45
# model_id=claude-opus-4-5
# provider=anthropic
# condition=predefined_primitives
# profile=empty
# task=S9
# run=5
# scene=['bread', 'bread bin']
# command=put the bread in its bin.
# generated=2026-08-05T06:59:14
# prompt_chars=15217
# tokens_in=4889 tokens_out=75
# seconds=5.9

confirm_before('put the bread in its bin')
put_first_on_second('bread', 'bread bin')
say_verified(lambda: is_in_bin('bread'),
             'The bread is in its bin.', 'The bread did not end up in its bin.')
pause_for_verification()
