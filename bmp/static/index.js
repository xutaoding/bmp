$(function() {
	$(".menu").mouseover(function() {
		$(".li_list").show();
	});
	$(".menu").mouseout(function() {
		$(".li_list").hide();
	});



	$(".col-md-offset-2 .table>tbody>tr>td>button,.applica button").click(function() {
		$(this).css('background-color','#e4e4e4').css('color','#333')
	});
});