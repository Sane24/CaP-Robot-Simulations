# model_key=claude45
# model_id=claude-opus-4-5
# provider=anthropic
# condition=baseline
# profile=sighted_assist
# task=L1
# run=3
# scene=['milk', 'bread', 'cereal', 'can', 'milk bin', 'bread bin', 'cereal bin', 'can bin']
# command=put every object in its matching bin, one at a time.
# generated=2026-08-05T03:49:44
# prompt_chars=12571
# tokens_in=4070 tokens_out=81
# seconds=2.0

say('Ok - putting each object in its matching bin')
put_first_on_second('milk', 'milk bin')
put_first_on_second('bread', 'bread bin')
put_first_on_second('cereal', 'cereal bin')
put_first_on_second('can', 'can bin')
