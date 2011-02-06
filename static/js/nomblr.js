$(function() {

	var recipe = false, edit = false;
	var stack = [];
	stack._push = stack.push;
	stack.push = function(selector) {
		var jq = $(selector);
		if ("none" != jq.css("display")) {
			jq.hide();
			stack._push(selector);
		}
	};
	stack._pop = stack.pop;
	stack.pop = function() {
		var selector = stack._pop();
		$(selector).show();
	};

	$("body header a.add").click(function() {
		stack.push("#recipe");
		stack.push("#edit");
		$("#add").show();
		scroll(0, 0);
		return false;
	});
	$("#add a.close").click(function() {
		$("#add").hide();
		stack.pop();
		return false;
	});

	$("#recipe a.close").live("click", function() {
		$("#recipe").hide();
		stack.pop();
		return false;
	});
	$("#recipe a.fullscreen").live("click", function() {
		$("#fullscreen").addClass("fullscreen");
		return false;
	});
	$("#recipe a.fullscreen-off").live("click", function() {
		$("#fullscreen").removeClass("fullscreen");
		return false;
	});

	$("#recipe a.edit").live("click", function() {
		stack.push("#recipe");
		$("#edit").show();
		return false;
	});

	$("#edit a.close").live("click", function() {
		$("#edit").hide();
		stack.pop();
		return false;
	});

	$("a.nom").click(function() {
		$("#ajax").load($(this).attr("href"), function() {
//			$("#recipe").show();
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
