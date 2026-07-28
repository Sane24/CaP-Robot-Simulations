# model_key=claude
# model_id=claude-opus-4-5
# provider=anthropic
# condition=baseline
# profile=baseline
# task=L1
# run=3
# scene=['milk', 'bread', 'cereal', 'can', 'milk bin', 'bread bin', 'cereal bin', 'can bin']
# command=put every object in its matching bin, one at a time.
# generated=2026-07-23T13:10:32
# prompt_chars=12493
# tokens_in=4054 tokens_out=66
# seconds=2.0

say('Ok - putting every object in its matching bin')
objects_to_sort = ['milk', 'bread', 'cereal', 'can']
for obj in objects_to_sort:
  put_first_on_second(obj, f'{obj} bin')
