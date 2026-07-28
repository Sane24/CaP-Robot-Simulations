# model_key=openai
# model_id=gpt-5.2
# provider=openai
# condition=baseline
# profile=blind_assist
# task=L1
# run=2
# scene=['milk', 'bread', 'cereal', 'can', 'milk bin', 'bread bin', 'cereal bin', 'can bin']
# command=put every object in its matching bin, one at a time.
# generated=2026-07-23T13:17:18
# prompt_chars=12569
# tokens_in=3268 tokens_out=76
# seconds=1.5

matches = {'milk': 'milk bin', 'bread': 'bread bin', 'cereal': 'cereal bin', 'can': 'can bin'}
for obj_name, bin_name in matches.items():
  say(f'Now placing the {obj_name} into the {bin_name}')
  put_first_on_second(obj_name, get_obj_pos(bin_name))
