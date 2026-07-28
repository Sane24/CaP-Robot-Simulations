# model_key=openai
# model_id=gpt-5.2
# provider=openai
# condition=baseline
# profile=sighted
# task=L4
# run=1
# scene=['milk', 'bread', 'cereal', 'can', 'milk bin', 'bread bin', 'cereal bin', 'can bin']
# command=put the milk and the cereal each in its bin.
# generated=2026-07-23T13:16:56
# prompt_chars=12520
# tokens_in=3260 tokens_out=56
# seconds=1.8

matches = {'milk': 'milk bin', 'cereal': 'cereal bin'}
say('Got it - placing the milk and the cereal in their bins')
for first, second in matches.items():
  put_first_on_second(first, get_obj_pos(second))
