
$(function() {
	
	$("#btn_submit").click(function() {
		
		var msg = "";
		if($("#name").val() == "")
			msg += "名称不能为空\n";
		
		if(msg != "")
			alert(msg);
		else {
			$.getJSON(
				"ajax_dataclass_add?name=" + encodeURIComponent($("#name").val()) + "&parent_id=" + $("#parent_id").val() + "&sort=" + $("#sort").val() + "&type=" + get_menu_param("type") + "&random=" + Math.random(),
				function(data) {
					
					//重置参数
					$("#menu_param").val("type:1");
					$("#center-column").load("../../static/simple/admin_templates/dataclass_list.html?random=" + Math.random());
				}
			);
		}	
		
		return false;
	});	
});
