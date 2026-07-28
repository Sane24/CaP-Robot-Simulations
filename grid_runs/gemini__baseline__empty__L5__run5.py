# model_key=gemini
# model_id=gemini-3.1-pro-preview
# provider=google
# condition=baseline
# profile=baseline
# task=L5
# run=5
# scene=['red block', 'green block', 'blue block', 'yellow block']
# command=put the blocks on different corners clockwise starting at the top right corner.
# generated=2026-07-28T08:37:12
# prompt_chars=12494
# tokens_in=3790 tokens_out=37
# seconds=8.6

block_names = parse_obj_name('the blocks', f'objects = {get_obj_names()}')
corners = parse_position('different corners clockwise starting at the
