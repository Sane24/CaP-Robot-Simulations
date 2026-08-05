# model_key=claude45
# model_id=claude-opus-4-5
# provider=anthropic
# condition=predefined_primitives
# profile=blind_assist
# task=L1
# run=5
# scene=['milk', 'bread', 'cereal', 'can', 'milk bin', 'bread bin', 'cereal bin', 'can bin']
# command=put every object in its matching bin, one at a time.
# generated=2026-08-05T07:25:57
# prompt_chars=15382
# tokens_in=4941 tokens_out=143
# seconds=3.5

objs = [o for o in get_obj_names() if not o.endswith(' bin')]
confirm_before('put every object in its matching bin')
for i, obj in enumerate(objs):
    say_progress(i + 1, len(objs), f'placing the {obj} in its bin')
    put_first_on_second(obj, f'{obj} bin')
    say_verified(lambda o=obj: is_in_bin(o),
                 f'The {obj} is in its bin.', f'The {obj} did not end up in its bin.')
