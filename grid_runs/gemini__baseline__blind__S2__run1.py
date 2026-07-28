# model_key=gemini
# model_id=gemini-3.1-pro-preview
# provider=google
# condition=baseline
# profile=blind
# task=S2
# run=1
# scene=['cube']
# command=lift the cube above the table.
# generated=2026-07-28T08:10:03
# prompt_chars=12428
# tokens_in=3778 tokens_out=40
# seconds=9.4

say('Ok - lifting the cube above the table')
target_pos = parse_position('a point above the table')
put_first_on_second('cube', target_pos
