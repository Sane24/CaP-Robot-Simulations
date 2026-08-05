# model_key=claude
# model_id=claude-opus-4-8
# provider=anthropic
# condition=baseline
# profile=blind
# task=S9
# run=3
# scene=['bread', 'bread bin']
# command=put the bread in its bin.
# generated=2026-08-05T02:42:06
# prompt_chars=12437
# tokens_in=5251 tokens_out=39
# seconds=2.0

say('Ok - putting the bread in the bread bin')
put_first_on_second('bread', 'bread bin')
