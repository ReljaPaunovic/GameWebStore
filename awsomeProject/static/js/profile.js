$(document).ready(function() {
$(".btn-pref .btn").click(function () {
    // $(".btn-pref .btn").removeClass("btn-primary").addClass("thumbnail");
    // $(".tab").addClass("active"); // instead of this do the below
	$(".btn-pref .btn").removeClass("btn-primary active").addClass("thumbnail");
    $(this).addClass("btn-primary active");
});

//$("#add-another-game-btn").click( function () {
	//location.reload();
	//$('#backend_upload').trigger("reset");
//});

});
