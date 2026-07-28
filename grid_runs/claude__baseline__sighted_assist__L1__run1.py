# model_key=claude
# model_id=claude-opus-4-5
# provider=anthropic
# condition=baseline
# profile=sighted_assist
# task=L1
# run=1
# scene=['milk', 'bread', 'cereal', 'can', 'milk bin', 'bread bin', 'cereal bin', 'can bin']
# command=put every object in its matching bin, one at a time.
# generated=2026-07-23T13:14:46
# prompt_chars=12571
# tokens_in=4070 tokens_out=127
# seconds=2.4

say('Ok - putting each object in its matching bin')
put_first_on_second('milk', 'milk bin')
say('Put the milk in the milk bin')
put_first_on_second('bread', 'bread bin')
say('Put the bread in the bread bin')
put_first_on_second('cereal', 'cereal bin')
say('Put the cereal in the cereal bin')
put_first_on_second('can', 'can bin')
say('Put the can in the can bin')
