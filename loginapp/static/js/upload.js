$(function() {
	
	$("#fileBrowseBtn").change(function() {
		//var fileName = $(this).val();
		if($('#fileBrowseBtn').val() != "") { 
			$("#uploadBtn").fadeIn(800);
		} else {
			$('#uploadBtn').hide();
		}
	});
});


$(document).ready( function(){
	
	$('#uploadBtn').hide();
});