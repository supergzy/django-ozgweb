
var menu_list = null;

//左边菜单（大类）的点击事件
function left_menu() {
	$("#left-column > .link").click(function() {
		$("#left-column > ul").attr("class", "navhide");

		$(this).next().attr("class", "nav");
		return false;
	});
}

$(function() {
	
	//上面的菜单
	$.getJSON(
		"ajax_menu_list",
		function(data) {
			menu_list = data.data;
			
			//上面的菜单
			$.each(menu_list, function(i, item_obj) {
				var item = null;
				
				if(item_obj.selected) {
					//选定
					item = '<li class="active"><span><span>' + item_obj.name + '</span></span></li>';
					
					//左边的大类
					$.each(item_obj.child_menu, function(j, item_obj_child) {
						$("#left-column").append('<a href="#" class="link">' + item_obj_child.name + '</a>');
						
						if(j == 0)							
							$("#left-column").append('<ul class="nav" id="child_menu_' + item_obj_child.id + '"></ul>'); //默认选定第一个											
						else
							$("#left-column").append('<ul class="navhide" id="child_menu_' + item_obj_child.id + '"></ul>');
						
						//左边大类下面的小类
						$.each(item_obj_child.child_menu, function(k, item_obj_child2) {
							var item_obj_child2 = item_obj_child.child_menu[k];
							
							if(k + 1 < item_obj_child.child_menu.length)
								$("#child_menu_" + item_obj_child.id).append('<li><a href="#">' + item_obj_child2.name + '</a></li>');
							else
								$("#child_menu_" + item_obj_child.id).append('<li class="last"><a href="#">' + item_obj_child2.name + '</a></li>'); //最后一个
						});
					});
				}
				else
					item = '<li><span><span><a href="#">' + item_obj.name + '</a></span></span>';
				$("#top-navigation").append(item);
			});
			
			left_menu();
		}
	);
	
});
