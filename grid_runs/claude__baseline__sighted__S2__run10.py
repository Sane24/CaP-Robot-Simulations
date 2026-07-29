# model_key=claude
# model_id=claude-opus-4-8
# provider=anthropic
# condition=baseline
# profile=sighted
# task=S2
# run=10
# scene=['cube']
# command=lift the cube above the table.
# generated=2026-07-28T12:06:10
# prompt_chars=12430
# tokens_in=5245 tokens_out=57
# seconds=1.9

say('Ok - lifting the cube above the table')
above_pos = parse_position('a point 10cm above the cube')
put_first_on_second('cube', above_pos)
