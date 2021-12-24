// document.getElementById('stop').style.visibility = 'hidden';
if(localStorage.getItem("btn_state")){
     document.getElementById('start_div').innerHTML=localStorage.getItem("btn_state")
}
   
if(localStorage.getItem("download_btn")){

    document.getElementById('download').style.visibility = 'visible';
}
else{

    document.getElementById('download').style.visibility = 'hidden';
}
function httpGet(theUrl)
{
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "GET", theUrl, false ); // false for synchronous request
    xmlHttp.send( null );
    return xmlHttp.responseText;
}
function qrcode(theUrl)
{
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "GET", theUrl, false ); // false for synchronous request
    xmlHttp.send( null );
    return xmlHttp.responseText;
}
function start() {
  $(document).ready(function(){
//   $.ajaxSetup({ cache: false });
  
//     $.getJSON('/accounts/server/start',function(rowz){
            getter=httpGet('/accounts/server/start');
            qrcode_generate=httpGet('/accounts/qrcode/generate');
           
            // document.getElementById('start').style.visibility = 'hidden';
        
            // document.getElementById('stop').style.visibility = 'visible';
//       var myfunc = setInterval(function() {
// // code goes here
// }, 1000)
// var starts = new Date().getTime();


           // var end = new Date().getTime();
           // var time = end - starts;
            // console.log(time)
            //             // var now = new Date().getTime();
            // var timeleft =  0;
            // console.log(timeleft)
           
            // var hours = Math.floor((timeleft % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
            // var minutes = Math.floor((timeleft % (1000 * 60 * 60)) / (1000 * 60));
            // var seconds = Math.floor((timeleft % (1000 * 60)) / 1000);
            // let time= document.getElementById('time');
            // time.innerHTML=`${hours}:${minutes}:${seconds}`
            let start= document.getElementById('start_div');
            start.innerHTML=''
        
            start.innerHTML='<button type="button" class="btn btn-danger" id="stop" onclick="stop();">Stop</button>';
            localStorage.setItem("btn_state",'<button type="button" class="btn btn-danger" id="stop" onclick="stop();">Stop</button>');
             alert("Qrcode is generated");
// });
   

});
}
function stop() {
  $(document).ready(function(){
  $.ajaxSetup({ cache: false });
  
    $.getJSON('server/stop',function(rowz){
   
                        
      
        
            // document.getElementById('stop').style.visibility = 'hidden';
            document.getElementById('download').style.visibility = 'visible';
            
            // document.getElementById('start').style.visibility = 'visible';
        
            let start= document.getElementById('start_div');
            start.innerHTML=''
        
            start.innerHTML='  <button type="button" class="btn btn-success" id="start" onclick="start();"> Start</button>';
            localStorage.setItem("btn_state",'  <button type="button" class="btn btn-success" id="start" onclick="start();"> Start</button>');
            localStorage.setItem("download_btn","visible");
});
   

});
}
