# model=openai condition=baseline profile=blind task=T1

say('Ok - putting the red block on the green block now. I will pick up the red block and place it directly on top of the green block, and I will tell you when it is done.')
put_first_on_second('red block', 'green block')
say('Done - the red block is now on top of the green block.')
