$(function () {
    var ctx = document.getElementById("myChart").getContext("2d");
    // examine example_data.json for expected response data
    var json_url = "/accounts/post/ajax/info";

         let labels = ['Number of Attendance', 'Absence number'];
         let colorHex = [ '#079bfe','#ff6384'];
         myChart = new Chart(ctx, {
            type: 'pie',
            data: {datasets: [{data:[] ,backgroundColor: colorHex}],labels: labels},
            plugins:[ChartDataLabels] ,
            options: {responsive: false,maintainAspectRatio: false,legend: {position: 'right'},
                  plugins:{
                    datalabels: {
                      color: '#000',
                      anchor: 'center',
                      align: 'center',
                      font: {weight: 'bold',size: '25'}}}}});
    setInterval(function() {
    ajax_chart(myChart, json_url);
    }, 1000);
    // function to update our chart
     
    function ajax_chart(chart, url, data) {
        var data = data || {};

        $.getJSON(url, data).done(function(response) {
            // chart.data.labels = response.labels;
            chart.data.datasets[0].data[0] = response.attendance_number; // or you can iterate for multiple datasets
            chart.data.datasets[0].data[1] = response.absence_number; // or you can iterate for multiple datasets
            chart.update(); // finally update our chart
        });
    }
});
