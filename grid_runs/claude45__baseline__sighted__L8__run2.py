# model_key=claude45
# model_id=claude-opus-4-5
# provider=anthropic
# condition=baseline
# profile=sighted
# task=L8
# run=2
# scene=['red block', 'green block', 'blue block', 'red bowl', 'green bowl', 'blue bowl']
# command=place the blocks in bowls with non-matching colors.
# generated=2026-08-05T03:43:16
# prompt_chars=12524
# tokens_in=4053 tokens_out=148
# seconds=3.8

block_names = ['red block', 'green block', 'blue block']
bowl_names = ['red bowl', 'green bowl', 'blue bowl']
say('Placing blocks in bowls with non-matching colors')
for block_name in block_names:
    block_color = block_name.split()[0]
    for bowl_name in bowl_names:
        bowl_color = bowl_name.split()[0]
        if block_color != bowl_color:
            put_first_on_second(block_name, bowl_name)
            bowl_names.remove(bowl_name)
            break
