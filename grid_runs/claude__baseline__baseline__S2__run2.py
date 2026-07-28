# model_key=claude
# model_id=claude-opus-4-5
# provider=anthropic
# condition=baseline
# profile=baseline
# task=S2
# run=2
# scene=['cube']
# command=lift the cube above the table.
# generated=2026-07-23T13:09:22
# prompt_chars=12395
# tokens_in=4014 tokens_out=47
# seconds=1.4

say('Ok - lifting the cube above the table')
target_pos = parse_position('a point 10cm above the cube')
put_first_on_second('cube', target_pos)
