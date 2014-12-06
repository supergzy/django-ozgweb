
$(function() {
	
	
	
	//添加按钮
	$("#add_btn").click(function() {
		$("#center-column").load("../../static/simple/admin_templates/dataclass_add.html?random=" + Math.random());
		return false;
	});	
});
