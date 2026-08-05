# model_key=claude45
# model_id=claude-opus-4-5
# provider=anthropic
# condition=predefined_primitives
# profile=sighted_assist
# task=L10
# run=3
# scene=['lemon', 'bottle', 'green plate', 'blue plate']
# command=move all fruits to the green plate and bottles to the blue plate.
# generated=2026-08-05T07:40:24
# prompt_chars=15361
# tokens_in=4924 tokens_out=221
# seconds=5.6

fruits = parse_obj_name('the fruits', f'objects = {get_obj_names()}')
bottles = parse_obj_name('the bottles', f'objects = {get_obj_names()}')
all_items = [(f, 'green plate') for f in fruits] + [(b, 'blue plate') for b in bottles]
confirm_before('move all fruits to the green plate and bottles to the blue plate')
for i, (obj, plate) in enumerate(all_items):
    say_progress(i + 1, len(all_items), f'placing the {obj} on the {plate}')
    put_first_on_second(obj, plate)
    say_verified(lambda o=obj, p=plate: is_on_plate(o, p),
                 f'The {obj} is on the {plate}.',
                 f'The {obj} did not end up on the {plate}.')
