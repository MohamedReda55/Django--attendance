
// function updateMsg(){
  
//   $.ajaxSetup({ cache: false});
//   $.getJSON('/accounts/post/ajax/info',function(rowz){
    
//       let ctx = document.getElementById('myChart').getContext('2d');
//       let labels = ['Number of Attendance', 'Absence number'];
//       let colorHex = [ '#079bfe','#ff6384'];
//       var subject_name=document.getElementById('sub')
//       subject_name.innerHTML = rowz["subject_name"] 
//       var attendance_number=rowz["attendance_number"]
//       var absence_number=rowz["absence_number"]
//       console.log(rowz)
//       let data=[attendance_number, absence_number]
//       myChart = new Chart(ctx, {
//             type: 'pie',
//             data: {datasets: [{data:data ,backgroundColor: colorHex}],labels: labels},
//             plugins:[ChartDataLabels] ,
//             options: {responsive: false,maintainAspectRatio: false,legend: {position: 'right'},
//                   plugins:{
//                     datalabels: {
//                       color: '#000',
//                       anchor: 'center',
//                       align: 'center',
//                       font: {weight: 'bold',size: '25'}}}}})
    
//     $.ajaxSetup({ cache: false});
//     setTimeout('updateMsg()',3000);
//     document.querySelector("#chartReport").innerHTML = '<canvas id="myChart"></canvas>';
//     });
//    }
//   $(document).ready(function(){
//       updateMsg()
// });    
let ctx = document.getElementById('myChart').getContext('2d');
function run_chart(data)
{
      let labels = ['Number of Attendance', 'Absence number'];
      let colorHex = [ '#079bfe','#ff6384'];
}
$(document).ready(function(){
  $.ajaxSetup({ cache: false });
  setInterval(function() {
    $.getJSON('/accounts/post/ajax/info',function(rowz){
        
      // let labels = ['Number of Attendance', 'Absence number'];
      // let colorHex = [ '#079bfe','#ff6384'];
      // var subject_name=document.getElementById('sub')
      // subject_name.innerHTML = rowz["subject_name"] 
      var attendance_number=rowz["attendance_number"]
      var absence_number=rowz["absence_number"]
      let data=[attendance_number, absence_number]
      var num=attendance_number.toString()
      if(localStorage.getItem("chart")!=num){
        document.querySelector("#chartReport").innerHTML = '<canvas id="myChart"></canvas>'; 
        // let ctx = document.getElementById('myChart').getContext('2d');
         myChart = new Chart(ctx, {
            type: 'pie',
            data: {datasets: [{data:data ,backgroundColor: colorHex}],labels: labels},
            plugins:[ChartDataLabels] ,
            options: {responsive: false,maintainAspectRatio: false,legend: {position: 'right'},
                  plugins:{
                    datalabels: {
                      color: '#000',
                      anchor: 'center',
                      align: 'center',
                      font: {weight: 'bold',size: '25'}}}}})
          localStorage.setItem("chart",num);
        //  document.querySelector("#chartReport").innerHTML = '<canvas id="myChart"></canvas>'; 
        //   document.querySelector("#chartReport").innerHTML = '<canvas id="myChart"></canvas>'; 
        // // let ctx = document.getElementById('myChart').getContext('2d');
        //  myChart = new Chart(ctx, {
        //     type: 'pie',
        //     data: {datasets: [{data:data ,backgroundColor: colorHex}],labels: labels},
        //     plugins:[ChartDataLabels] ,
        //     options: {responsive: false,maintainAspectRatio: false,legend: {position: 'right'},
        //           plugins:{
        //             datalabels: {
        //               color: '#000',
        //               anchor: 'center',
        //               align: 'center',
        //               font: {weight: 'bold',size: '25'}}}}})
        //      localStorage.setItem("chart",attendance_number+absence_number);
        }
      else
      { 
         
           
             

      } 

    
     
      
    });
    // document.querySelector("#chartReport").innerHTML = '<canvas id="myChart"></canvas>';
  }, 3000);

});