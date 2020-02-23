
addData.onclick = e => {
	if (''+Number(uah2.value) === uah2.value
		&& currDate.value != ''
		&& Number(uah2.value) >= 0) {
		visibilVisib(canvasContainer);
		console.log(uah2.value, currDate.value);
		// '2020-12-31' to 20201231
		intDateLabel = curChart.data.labels.forEach(function(el) {
				parseInt(el.split('-'))
			});
		firInd = indexOfFirstBiggerNum(currDate.value, curChart.data.labels)
		// insert value before first bigger value
		curChart.data.labels.splice(firInd, 0, currDate.value);
		curChart.data.datasets.forEach((dataset) => {
			dataset.data.splice(firInd, 0, uah2.value);
		});
		curChart.update();
	}
};


popData.onclick = e => {
	console.log(uah2.value, currDate.value);
	curChart.data.labels.pop();
	curChart.data.datasets.forEach((dataset) => {
		dataset.data.pop();
	});
	curChart.update();
	if (curChart.data.labels[0] == null) {
		visibilHidden(canvasContainer);
	}
};


function indexOfFirstBiggerNum(elem, arr) {
	for (var i = 0; i < arr.length; i++) {
		if (elem < arr[i]) {
			return i;
		}
	}
	return arr.length;
}
