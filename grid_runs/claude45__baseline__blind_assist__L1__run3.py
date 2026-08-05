# model_key=claude45
# model_id=claude-opus-4-5
# provider=anthropic
# condition=baseline
# profile=blind_assist
# task=L1
# run=3
# scene=['milk', 'bread', 'cereal', 'can', 'milk bin', 'bread bin', 'cereal bin', 'can bin']
# command=put every object in its matching bin, one at a time.
# generated=2026-08-05T03:46:01
# prompt_chars=12569
# tokens_in=4069 tokens_out=72
# seconds=2.6

objects_to_sort = ['milk', 'bread', 'cereal', 'can']
for obj in objects_to_sort:
  say(f'Putting the {obj} in the {obj} bin')
  put_first_on_second(obj, f'{obj} bin')
