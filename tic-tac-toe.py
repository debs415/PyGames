ctr=0
grid=[[' ',' ',' '],
[' ',' ',' '],
[' ',' ',' ']]
while(ctr<9):
	print('+-+-+-+')
	pretty_row = ''
	# '|O| |X|'
	# row = ['O', '', 'X']
	pretty_row = pretty_row + '|'
	pretty_row = pretty_row + grid[0][0]
	pretty_row = pretty_row + '|'
	pretty_row = pretty_row + grid[0][1]
	pretty_row = pretty_row + '|'
	pretty_row = pretty_row + grid[0][2]+'|'
	print(pretty_row)
	print('+-+-+-+')
	pretty_row = ''
	pretty_row = pretty_row + '|'
	pretty_row = pretty_row + grid[1][0]
	pretty_row = pretty_row + '|'
	pretty_row = pretty_row + grid[1][1]
	pretty_row = pretty_row + '|'
	pretty_row = pretty_row + grid[1][2]+'|'
	print(pretty_row)
	print('+-+-+-+')
	pretty_row = ''
	pretty_row = pretty_row + '|'
	pretty_row = pretty_row + grid[2][0]
	pretty_row = pretty_row + '|'
	pretty_row = pretty_row + grid[2][1]
	pretty_row = pretty_row + '|'
	pretty_row = pretty_row + grid[2][2]+'|'
	print(pretty_row)
	print('+-+-+-+')
	x=int(input('Enter the row no.'))
	y=int(input('Enter the column no'))
	if(ctr%2==0):
		grid[x][y]='o'
	else:
		grid[x][y]='X'
	ctr=ctr+1
	if(ctr>=3 and ctr<9):
		if(grid[0][0]=='X'and grid[1][1]=='X' and grid[2][2]=='X' or grid[0][0]=='X'and grid[0][1]=='X' and grid[0][2]=='X' or grid[1][0]=='X'and grid[1][1]=='X' and grid[1][2]=='X' or grid[2][0]=='X'and grid[2][1]=='X' and grid[2][2]=='X' or grid[2][0]=='X'and grid[1][1]=='X' and grid[0][2]=='X' or grid[1][0]=='X'and grid[2][0]=='X' and grid[0][0]=='X' or grid[1][1]=='X'and grid[2][1]=='X' and grid[0][1]=='X' or grid[0][2]=='X'and grid[1][2]=='X' and grid[2][2]=='X'):
			print('congratulations! player 1, u have won')
			break
		if(grid[0][0]=='o'and grid[1][1]=='o' and grid[2][2]=='o' or grid[0][0]=='o'and grid[0][1]=='o' and grid[0][2]=='o' or grid[1][0]=='o'and grid[1][1]=='o' and grid[1][2]=='o' or grid[2][0]=='o'and grid[2][1]=='o' and grid[2][2]=='o' or grid[2][0]=='o'and grid[1][1]=='o' and grid[0][2]=='o' or grid[1][0]=='o'and grid[2][0]=='o' and grid[0][0]=='o' or grid[1][1]=='o'and grid[2][1]=='o' and grid[0][1]=='o' or grid[0][2]=='o'and grid[1][2]=='o' and grid[2][2]=='o'):
			print('congratulations! player 2, u have won')
			break
	elif(ctr==9):
		print("Nobody wins")
	else:
		continue	

		