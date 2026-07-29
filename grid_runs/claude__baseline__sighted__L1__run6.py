# model_key=claude
# model_id=claude-opus-4-8
# provider=anthropic
# condition=baseline
# profile=sighted
# task=L1
# run=6
# scene=['milk', 'bread', 'cereal', 'can', 'milk bin', 'bread bin', 'cereal bin', 'can bin']
# command=put every object in its matching bin, one at a time.
# generated=2026-07-28T12:06:45
# prompt_chars=12528
# tokens_in=5294 tokens_out=166
# seconds=3.1

matches = parse_obj_name('the matching bin for each object', f'objects = {get_obj_names()}')
object_names = parse_obj_name('the objects that are not bins', f'objects = {get_obj_names()}')
say('Ok - putting every object in its matching bin')
for object_name in object_names:
  bin_name = parse_obj_name(f'the bin that matches the {object_name}', f'objects = {get_obj_names()}')
  put_first_on_second(object_name, bin_name)
