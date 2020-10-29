var ctx = document.getElementById("");
var myChart = new Chart(ctx, {
  type: 'line',
  data: {
    labels: time_range,
    datasets: [
    { 
  		data: prices,
  		label: "Price",
  		borderColor: "#3e95cd",
  		fill: false
	},
	{ 
  		data: market_cap,
  		label: "Market Cap",
  		borderColor: "#8e5ea2",
  		fill: false
	},
	{ 
  		data: total_volume,
  		label: "Total Volume",
  		borderColor: "#3cba9f",
  		fill: false
	}
    ]
  }
});
