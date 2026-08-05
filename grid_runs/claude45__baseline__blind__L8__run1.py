# model_key=claude45
# model_id=claude-opus-4-5
# provider=anthropic
# condition=baseline
# profile=blind
# task=L8
# run=1
# scene=['red block', 'green block', 'blue block', 'red bowl', 'green bowl', 'blue bowl']
# command=place the blocks in bowls with non-matching colors.
# generated=2026-08-05T03:39:24
# prompt_chars=12522
# tokens_in=4052 tokens_out=163
# seconds=3.4

block_names = parse_obj_name('the blocks', f'objects = {get_obj_names()}')
bowl_names = parse_obj_name('the bowls', f'objects = {get_obj_names()}')
say('Placing blocks in bowls with non-matching colors')
for block_name in block_names:
    block_color = block_name.split()[0]
    for bowl_name in bowl_names:
        bowl_color = bowl_name.split()[0]
        if block_color != bowl_color:
            put_first_on_second(block_name, bowl_name)
            bowl_names.remove(bowl_name)
            break
