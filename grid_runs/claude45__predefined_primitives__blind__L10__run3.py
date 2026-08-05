# model_key=claude45
# model_id=claude-opus-4-5
# provider=anthropic
# condition=predefined_primitives
# profile=blind
# task=L10
# run=3
# scene=['lemon', 'bottle', 'green plate', 'blue plate']
# command=move all fruits to the green plate and bottles to the blue plate.
# generated=2026-08-05T07:14:00
# prompt_chars=15316
# tokens_in=4915 tokens_out=219
# seconds=4.7

confirm_before('move all fruits to the green plate and bottles to the blue plate')
fruits = parse_obj_name('fruits', f'objects = {get_obj_names()}')
bottles = parse_obj_name('bottles', f'objects = {get_obj_names()}')
all_items = [(f, 'green plate') for f in fruits] + [(b, 'blue plate') for b in bottles]
for i, (obj, plate) in enumerate(all_items):
    say_progress(i + 1, len(all_items), f'placing the {obj} on the {plate}')
    put_first_on_second(obj, plate)
    say_verified(lambda o=obj, p=plate: is_on_plate(o, p),
                 f'The {obj} is on the {plate}.',
                 f'The {obj} did not end up on the {plate}.')
