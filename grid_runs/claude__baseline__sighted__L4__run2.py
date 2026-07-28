# model_key=claude
# model_id=claude-opus-4-5
# provider=anthropic
# condition=baseline
# profile=sighted
# task=L4
# run=2
# scene=['milk', 'bread', 'cereal', 'can', 'milk bin', 'bread bin', 'cereal bin', 'can bin']
# command=put the milk and the cereal each in its bin.
# generated=2026-07-23T13:13:45
# prompt_chars=12520
# tokens_in=4061 tokens_out=50
# seconds=2.0

say('Putting the milk and cereal in their bins')
put_first_on_second('milk', 'milk bin')
put_first_on_second('cereal', 'cereal bin')
