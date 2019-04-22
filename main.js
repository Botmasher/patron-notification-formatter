// example data
// TODO: scrape notifications
notificationsRaw = `
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
`;

// Notifications data restructure
// {
// 	date: {
// 		pledged: {
// 			amount: Set(...names),
// 			...
// 		},
// 		edited: {
// 			amount: Set(...names),
// 			...
// 		},
// 		deleted: {
// 			amount: Set(..names),
// 			...
// 		}
// 	},
// 	...
// }

class Notifications {
	constructor() {
		// restructured notifications object
		this.notifications = {};
		// terms to search for in the data
		this.status = {
			pledged: 'pledged by'
			deleted: 'deleted by',
			edited: 'edited by'
		};
	}

	// name, amount, status on first line and date on second
	parseLinePair = (lineWithName, lineWithDate, statusKey="") => {
		if (!modKey || !this.status[modKey]) return;

		// read first line for amount
		const amount = modKey === 'edited'
			? lineWithName.split(" ")[0] 	// index if pledged or deleted amounts
			: lineWithName.split(" ")[2]	// index if arrow from original to edited amount
		;
		
		// find the created/modified/removed verb phrase
		const statusString = this.status[statusKey];

		// read and clean up name from first line
		const name = lineWithName.substring(lineWithName.indexOf(statusString) + statusString.length).trim();
	
		this.notifications[formattedDate][statusKey][amount].push(name)
	};

	// Take a patrons notification list and format an object containing
	// dates, amounts, modification type and names
	restructure = rawText => {
		const lines = rawText.split("\n");
		// find and parse lines with new/modified patron status
		lines.map((line, i) => {
			const modKeys = Object.keys(this.status).filter(
				k => line.includes(this.status[k])
			);
			// parse current and next line - expect next line to contain date
			modKeys && parseLinePair(line, lines[i+1], statusKey=modKeys[0]);
		});
		return this.notifications;
	}
}
