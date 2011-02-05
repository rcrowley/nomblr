$(function() {
	var add = false, recipe = false;

	$("body header a.add").click(function() {
		var r = $("#recipe");
		if (recipe = "none" != r.css("display")) { r.hide(); }
		$("#add").show();
		scroll(0, 0);
		return false;
	});
	$("#add a.close").click(function() {
		$("#add").hide();
		if (recipe) { $("#recipe").show(); }
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

	$("a.nom").click(function() {
		$("#recipe").load($(this).attr("href"), function() {
			$("#recipe").show();
			scroll(0, 0);
		});
		return false;
	});

	$("a.follow, a.following").click(function() {
		var e = this;
		$.ajax({
			data: {},
			error: function(xhr, textStatus, errorThrown) {
				alert("Something went wrong.");
			},
			success: function(data, textStatus, xhr) {
				if ($(e).hasClass("follow")) {
					$("div.paper_top, a.follow").hide();
					$("a.following").show();
				}
				else if ($(e).hasClass("following")) {
					$("a.follow").show();
					$("a.following").hide();
				}
			},
			type: "POST",
			url: $(this).attr("href")
		});
		return false;
	});

});
