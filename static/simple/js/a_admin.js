
$(function() {
		
	$("#left-column > .link").click(function() {
		$("#left-column > ul").attr("class", "navhide");

		$(this).next().attr("class", "nav");
		return false;
	});

});
