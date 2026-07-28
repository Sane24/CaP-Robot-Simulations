# model_key=gemini
# model_id=gemini-3.1-pro-preview
# provider=google
# condition=baseline
# profile=sighted_assist
# task=S2
# run=4
# scene=['cube']
# command=lift the cube above the table.
# generated=2026-07-28T08:53:58
# prompt_chars=12473
# tokens_in=3785 tokens_out=38
# seconds=8.8

say('Ok - lifting the cube above the table')
target_pos = parse_position('a point 10cm above the cube')
put_first_on_second
