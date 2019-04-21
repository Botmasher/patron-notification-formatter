import re

notifications_raw = """
$2 pledged by Abc123
Apr 21st, 2019
$5 ➞ $10 edited by Gqll Xyz
Apr 21st, 2019
$2 pledged by Jun Smit
Apr 20st, 2019
$40 ➞ $100.11 edited by Josh K
Apr 20th, 2019
$25 deleted by Ma Bo
Apr 19th, 2019
$1 pledged by Xyz A12ask
Apr 19st, 2019
"""

# Notifications data restructure
# {
#		'date': {
#			'new': {
#				# amount : set(...names),
# 			...
#			},
#			'updated': {
#				# amount : set(...names).
# 			...
#			}
#		},
# 	...
# }

def structure_notifications(raw_text):
	"""Take a patrons notification list and format an object containing
	dates, amounts, modification type and names"""
	notifications = {}
	notifications_lines = raw_text.split("\n")

	for line_i, line_txt in enumerate(notifications_lines):	
		
		if not line_txt:
			continue

		split_line = line_txt.split()

		if "deleted" in line_txt:
			name = line_txt[re.search("deleted by", line_txt).end():].strip()
			amount = split_line[0]
			mod_key = 'deleted'

		elif " ➞ $" in line_txt and "edited" in line_txt:
			name = line_txt[re.search("edited by", line_txt).end():].strip()
			amount = split_line[2]
			mod_key = 'edited'

		elif line_txt[0] == "$" and "pledged" in line_txt:
			name = line_txt[re.search("pledged by", line_txt).end():].strip()
			amount = split_line[0]
			mod_key = 'pledged'
			#notifications['new'].setdefault(amount, set()).add(name)

		else:
			continue

		# only add date and modify notifications if reached pledge/edit/delete branch
		date = notifications_lines[line_i + 1].strip()
		notifications.setdefault(date, {
			'pledged': {},
			'edited': {},
			'deleted': {}
		})
		notifications[date][mod_key].setdefault(amount, []).append(name)

	return notifications

def pretty_print_notifications(notifications, by_date=True):
	"""Print a formatted notifications object to console"""
	if not by_date:
		# TODO: reduce dict and print all in mods, amounts, names
		normalized_notifications = {
			'pledged': {},
			'edited': {},
			'deleted': {}
		}
		for date in notifications:
			for mod_type in notifications[date]:
				for amount in notifications[date][mod_type]:
					normalized_notifications[mod_type].setdefault(amount, [])
					normalized_notifications[mod_type][amount] += notifications[date][mod_type][amount]
		
		for modification_type in normalized_notifications:
			print(f"  {modification_type}:")
			amounts = [float(k[1:].strip()) for k in normalized_notifications[modification_type]]
			sorted_amounts = list(sorted(amounts))
			for amount in sorted_amounts:
				formatted_amount = f"${int(amount) if amount / int(amount) == 1.0 else amount}"
				names = normalized_notifications[modification_type][formatted_amount]
				print(f"    * {formatted_amount}:")
				[print(f"        {name}") for name in names]

		return

	for date in notifications:
		print(f"{date}:")
		for modification_type in notifications[date]:
			print(f"  {modification_type}:")
			for amount in notifications[date][modification_type]:
				names = notifications[date][modification_type][amount]
				print(f"    * {amount}:")
				[print(f"        {name}") for name in names]

notifications = structure_notifications(notifications_raw)
pretty_print_notifications(notifications, False)
