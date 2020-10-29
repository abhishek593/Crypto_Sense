new Chart(document.getElementById(""), {
    type: 'bar',
    data: {
      labels: coins,
      datasets: [
        {
          label: "Price",
          backgroundColor: "#3e95cd",
          data: prices
        }, {
          label: "Market Cap",
          backgroundColor: "#8e5ea2",
          data: market_cap
        }
      ]
    },
    options: {
      title: {
        display: true,
        text: 'Comparison on a particular date'
      }
    }
});
