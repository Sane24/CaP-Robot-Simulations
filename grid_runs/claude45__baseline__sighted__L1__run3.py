# model_key=claude45
# model_id=claude-opus-4-5
# provider=anthropic
# condition=baseline
# profile=sighted
# task=L1
# run=3
# scene=['milk', 'bread', 'cereal', 'can', 'milk bin', 'bread bin', 'cereal bin', 'can bin']
# command=put every object in its matching bin, one at a time.
# generated=2026-08-05T03:42:05
# prompt_chars=12528
# tokens_in=4062 tokens_out=80
# seconds=1.9

say('Putting every object in its matching bin')
put_first_on_second('milk', 'milk bin')
put_first_on_second('bread', 'bread bin')
put_first_on_second('cereal', 'cereal bin')
put_first_on_second('can', 'can bin')
