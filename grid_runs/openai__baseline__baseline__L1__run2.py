# model_key=openai
# model_id=gpt-5.2
# provider=openai
# condition=baseline
# profile=baseline
# task=L1
# run=2
# scene=['milk', 'bread', 'cereal', 'can', 'milk bin', 'bread bin', 'cereal bin', 'can bin']
# command=put every object in its matching bin, one at a time.
# generated=2026-07-23T13:15:38
# prompt_chars=12493
# tokens_in=3254 tokens_out=77
# seconds=1.9

matches = {'milk': 'milk bin', 'bread': 'bread bin', 'cereal': 'cereal bin', 'can': 'can bin'}
say('Got it - putting every object in its matching bin, one at a time')
for obj_name, bin_name in matches.items():
  put_first_on_second(obj_name, get_obj_pos(bin_name))
