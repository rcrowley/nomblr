$(function() {

	$("body header a.add").click(function() {
		$("#add").show();
		return false;
	});
	$("#add a.close").click(function() {
		$("#add").hide();
		return false;
	});

	$("#recipe a.close").click(function() {
		$("#recipe").hide();
		return false;
	});
	$("#recipe a.fullscreen").click(function() {
		$("#recwindow").addClass("recfull");
		return false;
	});
	$("#recipe a.fullscreen_off").click(function() {
		$("#recwindow").removeClass("recfull");
		return false;
	});

});
