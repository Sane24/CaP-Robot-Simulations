# model_key=openai
# model_id=gpt-5.2
# provider=openai
# condition=baseline
# profile=baseline
# task=L1
# run=1
# scene=['milk', 'bread', 'cereal', 'can', 'milk bin', 'bread bin', 'cereal bin', 'can bin']
# command=put every object in its matching bin, one at a time.
# generated=2026-07-23T13:15:36
# prompt_chars=12493
# tokens_in=3254 tokens_out=77
# seconds=1.8

say('Got it - putting every object in its matching bin, one at a time')
matches = {'milk': 'milk bin', 'bread': 'bread bin', 'cereal': 'cereal bin', 'can': 'can bin'}
for obj_name, bin_name in matches.items():
  put_first_on_second(obj_name, get_obj_pos(bin_name))
