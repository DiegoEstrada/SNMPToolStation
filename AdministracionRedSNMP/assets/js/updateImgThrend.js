$( document ).ready(function() {
  console.log( "ready!" );

  $("#btnCPU").click(function(){
    //alert("BEFORE")
    $.ajax({url: "Actualiza", success: function(result){
     // alert("AJAX" +result);
     
     //alert(result)
     document.getElementById("imgCPU").src = "/static/DiegoEGCPU.png"
      //$("#imgCPU").attr("src",result);
      console.log("Inside AJAX A "+result)
    }});
  });


});

