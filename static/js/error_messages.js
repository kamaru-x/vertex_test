$(document).ready(function(){
    // console.log('error wors')
	$('#part_number').change(function(e){
		e.preventDefault()
		let part_number = $('#part_number').val()
        // console.log('worked consolelog')
		// alert(cat_id)
		console.log(part_number)
		mydata = {'name':part_number}

		$.ajax({
			url : '/c-p/',
			type : 'POST',
			data : mydata,
			success : function(data){
				console.log(data)
                if(data.status==false){
                    alert('Part Number Already exists')
                    // $('#part_number').css('border-color', 'red');
                    // $('#part_number').css('border-width', '2px');
                }else{
                    
                }
			}
		})
	})
})