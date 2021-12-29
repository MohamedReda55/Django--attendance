$(function () {
    var ctx = document.getElementById("mybar").getContext("2d");
    // examine example_data.json for expected response data
    var json_url = "/accounts/post/ajax/info";
    const labels =["10/10","10/17","10/24","11/1","11/8","11/15","11/22","11/29","12/5","12/12","12/19","12/26"]
         myChart = new Chart(ctx, {
            type: 'bar',
            data : {
        labels: labels,
        datasets: [{
    //label: 'My First Dataset',
    data: [200, 250, 100, 400, 70, 20, 40,50,120,150,400,200],
    backgroundColor: [
      'rgba(255, 99, 132, 0.2)',
      'rgba(255, 159, 64, 0.2)',
      'rgba(255, 205, 86, 0.2)',
      'rgba(75, 192, 192, 0.2)',
      'rgba(54, 162, 235, 0.2)',
      'rgba(153, 102, 255, 0.2)',
      'rgba(201, 203, 207, 0.2)'
    ],
    borderColor: [
      'rgb(255, 99, 132)',
      'rgb(255, 159, 64)',
      'rgb(255, 205, 86)',
      'rgb(75, 192, 192)',
      'rgb(54, 162, 235)',
      'rgb(153, 102, 255)',
      'rgb(201, 203, 207)'
    ],
    borderWidth: 1
  }]
}, options: {
    plugins: {
    legend: {
      display: false
    }
  },

    maintainAspectRatio:false,
    scales: {
      y: {
        beginAtZero: true
      }
    }
  }
});
    setInterval(function() {
    // ajax_chart(myChart, json_url);
    }, 1000);
    // // function to update our chart
     
    // function ajax_chart(chart, url, data) {
    //     var data = data || {};

    //     // $.getJSON(url, data).done(function(response) {
    //     //     // chart.data.labels = response.labels;
    //     //     chart.data.datasets[0].data[0] = response.attendance_number; // or you can iterate for multiple datasets
    //     //     chart.data.datasets[0].data[1] = response.absence_number; // or you can iterate for multiple datasets
    //     //     chart.update(); // finally update our chart
    //     // });
    // }
});
