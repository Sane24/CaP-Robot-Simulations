# model_key=openai
# model_id=gpt-5.2
# provider=openai
# condition=baseline
# profile=sighted_assist
# task=L1
# run=1
# scene=['milk', 'bread', 'cereal', 'can', 'milk bin', 'bread bin', 'cereal bin', 'can bin']
# command=put every object in its matching bin, one at a time.
# generated=2026-07-23T13:17:48
# prompt_chars=12571
# tokens_in=3269 tokens_out=92
# seconds=1.7

matches = {'milk': 'milk bin', 'bread': 'bread bin', 'cereal': 'cereal bin', 'can': 'can bin'}
say('Got it - putting each item into its matching bin one at a time')
for obj_name, bin_name in matches.items():
  say(f'Putting the {obj_name} in the {bin_name}')
  put_first_on_second(obj_name, get_obj_pos(bin_name))
