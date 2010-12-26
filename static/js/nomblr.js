$(function() {

	$("body header a.add").click(function() {
		$("#add").show();
		return false;
	});
	$("#add a.close").click(function() {
		$("#add").hide();
		return false;
	});

	$("#recipe a.close").live("click", function() {
		$("#recipe").hide();
		return false;
	});
	$("#recipe a.fullscreen").live("click", function() {
		$("#recwindow").addClass("recfull");
		return false;
	});
	$("#recipe a.fullscreen_off").live("click", function() {
		$("#recwindow").removeClass("recfull");
		return false;
	});

	$("a.recipe").click(function() {
		$("#recipe").load($(this).attr("href"), function() {
			$("#recipe").show();
		});
		return false;
	});

});
