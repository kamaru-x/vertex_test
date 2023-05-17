$(document).ready(function(){

    proposal = $('#proposal').val()

    // function for showing category related products
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

    $('#discount_amount , #table ,#product_total').change(function(e){
        e.preventDefault()
        let method_id = $('#method').val()
        let discount_amount = $('#discount_amount').val()
        let = total_amount = $('#product_total').html()
        if (method_id == 1){
            new_discount = (total_amount-discount_amount)
            $('#temp_discount').html(discount_amount)
            $('#temp_grand').html(new_discount)
        }else if(method_id == 2){
            p = (total_amount*discount_amount)/100
            new_discount = total_amount-p
            $('#temp_discount').html(p)
            $('#temp_grand').html(new_discount)
        }

        mydata = {'proposal':proposal,'method':method_id,'discount':discount_amount,'grand':new_discount}

        $.ajax({
            url : '/add_percentage/',
            type : 'POST',
            data : mydata,
            success : function(data){
                console.log('Status:',data)
            }
        })
    })

    // percentage and discount calculation
    // let current_method = $('#current_method').val()
    // if (current_method == 2){

    //     var grand_total = $('#product_total').html()
    //     var percentage = $('#discount_percentage').val()
    //     p = (grand_total*percentage) / 100
    //     grand = grand_total - p
    //     $('#desplay').val(p)
    //     $('#temp_discount').html(p)

    // }

    // function set_temp(){
    //     let temp_total = $('#product_total').html()
    //     let temp_discount = $('#discount_percentage').val()
    //     let temp_method = $('#method').val()
    //     let temp_grand = temp_total
    //     if(temp_method == 1){
    //         temp_grand = temp_total - temp_discount
    //         $('#temp_grand').html(temp_grand)
    //         $('#temp_discount').html(temp_discount)
    //         $('#grand_total').val(temp_grand)
    //         $('#current_value').val(temp_grand)
    //     }else if(temp_method == 2){
    //         let result = $('#desplay').val()
    //         temp_grand = temp_total - result
    //         $('#temp_grand').html(temp_grand)
    //         $('#temp_discount').html(result)
    //         $('#current_value').val(temp_grand)
    //         $('#grand_total').val(temp_grand)
    //     }
    // }

    // set_temp()

    // new script for discount grandtotal and percentage

    // save percentage and discount without reloading
    $('#discount_percentage').change(function(){
        var grand_total = $('#product_total').html()
        var percentage = $('#discount_percentage').val()
        var method = $('#method').val()
        let proposal = $('#ProposalId').val()
        p = (grand_total*percentage) / 100
        grand = grand_total - p
        $('#desplay').val(p)

        mydata = {'proposal':proposal,'method':method,'discount':percentage}

        alert(mydata)

        $.ajax({
            url : '/add_percentage/',
            type : 'POST',
            data : mydata,
            success : function(data){
                console.log('Status:',data)
                set_temp()
            }
        })
    })
})