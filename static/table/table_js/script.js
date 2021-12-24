$(document).ready(function(){
  $.ajaxSetup({ cache: false });
  setInterval(function() {
    $.getJSON('/accounts/post/ajax/data',function(rowz){
       $('#mytable').empty();
      var table = document.getElementById('mytable')
      var subject_name=document.getElementById('sub')
      //var date=document.getElementById('date')
      //var time=document.getElementById('time')
      
      subject_name.innerHTML = rowz["subject_name"]      
           
      //date.innerHTML = rowz["date"]
      for (var i=0;i<rowz['students'].length;i++){
          arow=rowz['students'][i];
        	var row = `<tr>
							<td>${arow[0]}</td>
							<td>${arow[1]}</td>
							
					  </tr>`
			    table.innerHTML += row
       
      }
      
    });
    
  }, 3000);

});



// function updateMsg(){
    
//     $.ajaxSetup({ cache: true});
//     $.getJSON('/accounts/post/ajax/data',function(rowz){
//       console.log("JSON",rowz)
//       $('#mytable').empty();
//       var table = document.getElementById('mytable')
//       var subject_name=document.getElementById('sub')
//       //var date=document.getElementById('date')
//       //var time=document.getElementById('time')
      
//       subject_name.innerHTML = rowz["subject_name"]      
           
//       //date.innerHTML = rowz["date"]
//       for (var i=0;i<rowz['students'].length;i++){
//           arow=rowz['students'][i];
//         	var row = `<tr>
// 							<td>${arow[0]}</td>
// 							<td>${arow[1]}</td>
							
// 					  </tr>`
// 			    table.innerHTML += row
       
//       }
//       setTimeout('updateMsg()',3000);
//       $.ajaxSetup({ cache: false});
//     });
//   }
//   $(document).ready(function(){
//       updateMsg()
// });    