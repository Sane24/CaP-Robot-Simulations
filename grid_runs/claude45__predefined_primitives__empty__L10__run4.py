# model_key=claude45
# model_id=claude-opus-4-5
# provider=anthropic
# condition=predefined_primitives
# profile=empty
# task=L10
# run=4
# scene=['lemon', 'bottle', 'green plate', 'blue plate']
# command=move all fruits to the green plate and bottles to the blue plate.
# generated=2026-08-05T07:04:48
# prompt_chars=15283
# tokens_in=4906 tokens_out=227
# seconds=4.2

confirm_before('move all fruits to the green plate and bottles to the blue plate')
fruit_names = parse_obj_name('fruits', f'objects = {get_obj_names()}')
bottle_names = parse_obj_name('bottles', f'objects = {get_obj_names()}')
all_items = [(f, 'green plate') for f in fruit_names] + [(b, 'blue plate') for b in bottle_names]
for i, (obj, plate) in enumerate(all_items):
    say_progress(i + 1, len(all_items), f'placing the {obj} on the {plate}')
    put_first_on_second(obj, plate)
    say_verified(lambda o=obj, p=plate: is_on_plate(o, p),
                 f'The {obj} is on the {plate}.',
                 f'The {obj} did not end up on the {plate}.')
