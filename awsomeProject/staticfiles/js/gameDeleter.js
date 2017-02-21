//$("#deleteButton").click(function(){
//  alert("Clicked!");
//  click: True;
//});

$(document).ready(function () {
  $('#deleteButton').click(function () {
    alert("Hello, S");
  });
});
$(function(){
     $('form').on('submit', function(e){
         e.preventDefault();
         $.ajax({
             url: $(this).attr('action'),
             method: $(this).attr('method'),
             success: function(data){ $('#target').html(data) }
         });
     });
});
