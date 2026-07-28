# model_key=openai
# model_id=gpt-5.2
# provider=openai
# condition=baseline
# profile=sighted_assist
# task=L4
# run=2
# scene=['milk', 'bread', 'cereal', 'can', 'milk bin', 'bread bin', 'cereal bin', 'can bin']
# command=put the milk and the cereal each in its bin.
# generated=2026-07-23T13:17:59
# prompt_chars=12563
# tokens_in=3267 tokens_out=46
# seconds=1.1

say('Sure - putting the milk in the milk bin and the cereal in the cereal bin')
put_first_on_second('milk', 'milk bin')
put_first_on_second('cereal', 'cereal bin')
