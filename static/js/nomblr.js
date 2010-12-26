$(function() {

	$("body header a.add").click(function() {
		$("#add").show();
		return false;
	});
	$("#add a.close").click(function() {
		$("#add").hide();
		return false;
	});

});
