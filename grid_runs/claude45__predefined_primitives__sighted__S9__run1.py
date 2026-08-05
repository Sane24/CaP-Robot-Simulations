# model_key=claude45
# model_id=claude-opus-4-5
# provider=anthropic
# condition=predefined_primitives
# profile=sighted
# task=S9
# run=1
# scene=['bread', 'bread bin']
# command=put the bread in its bin.
# generated=2026-08-05T07:17:31
# prompt_chars=15252
# tokens_in=4899 tokens_out=75
# seconds=3.0

confirm_before('put the bread in its bin')
put_first_on_second('bread', 'bread bin')
say_verified(lambda: is_in_bin('bread'),
             'The bread is in its bin.', 'The bread did not end up in its bin.')
pause_for_verification()
