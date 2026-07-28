# model_key=openai
# model_id=gpt-5.2
# provider=openai
# condition=baseline
# profile=blind_assist
# task=L4
# run=2
# scene=['milk', 'bread', 'cereal', 'can', 'milk bin', 'bread bin', 'cereal bin', 'can bin']
# command=put the milk and the cereal each in its bin.
# generated=2026-07-23T13:17:29
# prompt_chars=12561
# tokens_in=3266 tokens_out=59
# seconds=1.4

matches = {'milk': 'milk bin', 'cereal': 'cereal bin'}
say('Got it - putting the milk in the milk bin, and the cereal in the cereal bin')
for first, second in matches.items():
  put_first_on_second(first, second)
