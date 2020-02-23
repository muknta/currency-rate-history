
var chrt = document.getElementById('currChart');
var curChart = null;
function setCurrData(labels=[], data=[]) {
	curChart = new Chart(chrt, {
	  type: 'line',
	  data: {
	    labels: labels,
	    datasets: [{
	    	data: data
	    }]
	  },
	  options: {
	    title: {
	      display: true,
	      text: 'Currency fluctuations chart'
	    },
	    legend: {
	    	display: false
	    },
	  	tooltips: {
			callbacks: {
			  	label: function(tooltipItem) {
		    		return tooltipItem.yLabel;
		    	}
			}
	  	},
	  	scales: {
	        yAxes: [{
	            ticks: {
	                suggestedMin: 0
	            }
	        }]
	    }
	  }
	});
	if (labels[0] != null & data[0] != null) {
		visibilVisib(canvasContainer);
	} else {
		visibilHidden(canvasContainer);
	}
}

setCurrData();


function visibilHidden(obj) {
    obj.style.visibility = 'hidden';
};
function visibilVisib(obj) {
    obj.style.visibility = 'visible';
};

