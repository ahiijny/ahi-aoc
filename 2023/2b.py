from math import prod

powers = []
max_amounts = {
	'red': 12,
	'green': 13,
	'blue': 14
}
while True:
	try:
		line = input()
		if not line:
			continue
		data = line.split(':')
		game_id = int(data[0].split()[1])
		draws = data[1].split(";")
		max_cols = {}
		for draw in draws:
			cols = {}
			colors = draw.split(",")
			for color in colors:
				color = color.strip()
				col_data = color.split()
				col_num = int(col_data[0].strip())
				col_name = col_data[1].strip()
				cols[col_name] = col_num
				if col_name not in max_cols:
					max_cols[col_name] = col_num
				else:
					max_cols[col_name] = max(max_cols[col_name], col_num)
		print(f"game {game_id}: {max_cols}")
		power = prod(max_cols.values())
		powers.append(power)
	except EOFError:
		break
		
print(f"powers: {powers}")

print(f"powers: {sum(powers)}")
