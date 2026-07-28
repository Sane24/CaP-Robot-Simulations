# model_key=gemini
# model_id=gemini-3.1-pro-preview
# provider=google
# condition=baseline
# profile=sighted_assist
# task=S2
# run=5
# scene=['cube']
# command=lift the cube above the table.
# generated=2026-07-28T08:54:07
# prompt_chars=12473
# tokens_in=3785 tokens_out=39
# seconds=8.8

say('Ok - lifting the cube above the table')
target_pos = parse_position('a point above the table')
put_first_on_second('cube', target_
