# model_key=openai
# model_id=gpt-5.2
# provider=openai
# condition=baseline
# profile=baseline
# task=L4
# run=1
# scene=['milk', 'bread', 'cereal', 'can', 'milk bin', 'bread bin', 'cereal bin', 'can bin']
# command=put the milk and the cereal each in its bin.
# generated=2026-07-23T13:15:46
# prompt_chars=12485
# tokens_in=3252 tokens_out=57
# seconds=1.6

matches = {'milk': 'milk bin', 'cereal': 'cereal bin'}
say('Got it - putting the milk and the cereal each in its bin')
for first, second in matches.items():
  put_first_on_second(first, get_obj_pos(second))
