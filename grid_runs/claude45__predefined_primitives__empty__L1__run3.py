# model_key=claude45
# model_id=claude-opus-4-5
# provider=anthropic
# condition=predefined_primitives
# profile=empty
# task=L1
# run=3
# scene=['milk', 'bread', 'cereal', 'can', 'milk bin', 'bread bin', 'cereal bin', 'can bin']
# command=put every object in its matching bin, one at a time.
# generated=2026-08-05T07:00:34
# prompt_chars=15306
# tokens_in=4924 tokens_out=143
# seconds=10.9

objs = [o for o in get_obj_names() if not o.endswith(' bin')]
confirm_before('put every object in its matching bin')
for i, obj in enumerate(objs):
    say_progress(i + 1, len(objs), f'placing the {obj} in its bin')
    put_first_on_second(obj, f'{obj} bin')
    say_verified(lambda o=obj: is_in_bin(o),
                 f'The {obj} is in its bin.', f'The {obj} did not end up in its bin.')
