$(document).ready(function(){
	$('#category').change(function(e){
		e.preventDefault()
		let cat_id = $('#category').val()
		// alert(cat_id)
		
		mydata = {'cat':cat_id}

		$.ajax({
			url : '/g-p/',
			type : 'POST',
			data : mydata,
			success : function(data){
				console.log('Status:',data)
				$('#product').html(data)
			}
		})
	})

	// $('#product').change(function(e){
	// 	e.preventDefault()
    //     let pro_id = $('#product').val()

    //     mydata = {'id':pro_id}

    //     $.ajax({
    //     	url : "/g-p-d/",
    //     	type : 'POST',
    //     	data : mydata,
    //     	success : function(data){
    //     		console.log('Status:',data)

    //     		$('#p_p').val(data.sprice)
    //     		$('#p_q').val(1)
    //             if(data.sprice){
    //                 $('#s_p').val(data.sprice)
    //             }else{
    //                 $('#s_p').val(data.pprice)
    //             }
    //     		$('#total').val(data.sprice)


    //     		$('#p_q').change(function(){
    //     			q = $('#p_q').val()
    //                 s = $('#s_p').val()
    //     			total = (s*q)

    //     			$('#total').val(total)
    //     		})

    //             $('#s_p').change(function(){
    //     			q = $('#p_q').val()
    //                 s = $('#s_p').val()
    //     			total = (s*q)

    //     			$('#total').val(total)
    //     		})
    //     	}
    //     })
    // })
})