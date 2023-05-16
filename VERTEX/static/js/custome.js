$(document).ready(function(){

	var calculated_total_sum = 0
	var rowCount = $('#mytable tr').length;
	var row = rowCount - 2

	for(i=1; i <= row; i++){
		var total = $('.total-'+i).html()
		// alert(total)
		calculated_total_sum += parseFloat(total)
	}

	$('#total_sum_value').html(calculated_total_sum)
    $('#grand_total').val(calculated_total_sum)

	var category_name = $('#category-name').html()
	
})