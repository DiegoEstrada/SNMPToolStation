$( document ).ready(function() {
  console.log( "ready!" );

  $("#btnCPU").click(function(){
    //alert("BEFORE")
    $.ajax({url: "Actualiza", success: function(result){
     // alert("AJAX" +result);
      $("#imgCPU").attr("src","/static/DiegoEGCPU.png");
      //$("#div1").html(result);
    }});
  });


});

