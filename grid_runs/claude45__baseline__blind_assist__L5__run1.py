# model_key=claude45
# model_id=claude-opus-4-5
# provider=anthropic
# condition=baseline
# profile=blind_assist
# task=L5
# run=1
# scene=['red block', 'green block', 'blue block', 'yellow block']
# command=put the blocks on different corners clockwise starting at the top right corner.
# generated=2026-08-05T03:47:42
# prompt_chars=12570
# tokens_in=4053 tokens_out=122
# seconds=5.4

say('Placing blocks on the corners clockwise starting from the top right corner')
corners = parse_position('the corners clockwise starting at the top right corner')
block_names = parse_obj_name('the blocks', f'objects = {get_obj_names()}')
for block_name, corner in zip(block_names, corners):
    say(f'Placing the {block_name} on the {get_corner_name(corner)}')
    put_first_on_second(block_name, corner)
