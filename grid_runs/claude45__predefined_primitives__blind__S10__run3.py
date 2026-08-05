# model_key=claude45
# model_id=claude-opus-4-5
# provider=anthropic
# condition=predefined_primitives
# profile=blind
# task=S10
# run=3
# scene=['cereal', 'cereal bin']
# command=put the object in its bin.
# generated=2026-08-05T07:08:57
# prompt_chars=15253
# tokens_in=4900 tokens_out=81
# seconds=2.3

confirm_before('put the cereal in its bin')
put_first_on_second('cereal', 'cereal bin')
say_verified(lambda: is_in_bin('cereal'),
             'The cereal is in its bin.', 'The cereal did not end up in its bin.')
pause_for_verification()
