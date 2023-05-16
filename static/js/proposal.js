$(document).ready(function(){
    
    // $('#desplay').show()

    let current_method = $('#current_method').val()
    if (current_method == 2){

        var grand_total = $('#product_total').html()
        var percentage = $('#discount_percentage').val()
        p = (grand_total*percentage) / 100
        grand = grand_total - p
        $('#desplay').val(p)
        $('#temp_discount').html(p)

    }

    function set_temp(){
        let temp_total = $('#product_total').html()
        let temp_discount = $('#discount_percentage').val()
        let temp_method = $('#method').val()
        let temp_grand = temp_total
        if(temp_method == 1){
            temp_grand = temp_total - temp_discount
            $('#temp_grand').html(temp_grand)
            $('#temp_discount').html(temp_discount)
            $('#grand_total').val(temp_grand)
            $('#current_value').val(temp_grand)
        }else if(temp_method == 2){
            let result = $('#desplay').val()
            temp_grand = temp_total - result
            $('#temp_grand').html(temp_grand)
            $('#temp_discount').html(result)
            $('#current_value').val(temp_grand)
            $('#grand_total').val(temp_grand)
        }
    }

    set_temp()

    $('#AddProduct').click(function(e){
        e.preventDefault()

        let output = ''
        let out_total = 0

        let product = $('#product').val()
        let proposal = $('#ProposalId').val()
        let price = $('#s_p').val()
        let quantity = $('#p_q').val()
        let total = $('#total').val()

        mydata = {'product':product,'proposal':proposal,'price':price,'quantity':quantity,'total':total}

        $.ajax({
            url : '/add-proposal-product/',
            type : 'POST',
            data : mydata,
            success : function(data){
                console.log('Status:',data)
                x = data.products
                let out_total = 0
                if(data.status == "saved"){
                    for(i=0; i<x.length; i++){
                        output += '<tr class="intro-x"><td class="w-40"><a href="" class=" whitespace-nowrap">'+i+
                            '</a></td><td class="w-40"><a href="" class="font-medium whitespace-nowrap">'+x[i].reference+
                            '</a></td><td><div class="whitespace-nowrap">'+x[i].name+
                            '</div></td><td class="w-64"><div>'+x[i].category+
                            '</div></td><td class="w-64"><div>'+x[i].price+
                            '</div></td><td class="w-64"><div>'+x[i].quantity+
                            '</div></td><td class="w-64"><div id="total" class="total-'+i+'">'+x[i].total+
                            '</div></td><td class="table-report__action"><div class="flex justify-center items-center"><a class="flex items-center text-danger whitespace-nowrap" style="cursor: pointer;" onclick="pop('+x[i].id+')" data-tw-toggle="modal" data-tw-target="#delete-confirmation-modal"><i data-lucide="trash" class="w-4 h-4 mr-1"></i> Remove</a></div></td></tr>'
                        out_total += x[i].total
                    }
                    $('#product_total').html(out_total)
                    $('#grand_total').val(out_total)
                    $('#current_value').val(out_total)
                    $("#mytablebody").html(output)
                    // $("#product-form")[0].reset()
                    $('#p_p').val(null)
                    $('#s_p').val(null)
                    $('#p_q').val(null)
                    $('#total').val(null)
                    var grand_total = $('#product_total').html()
                    $('#temp_grand').html(grand_total)
                    set_temp()
                }
            }
        })
    })

    $('#discount_percentage').change(function(){
        var grand_total = $('#product_total').html()
        var percentage = $('#discount_percentage').val()
        var method = $('#method').val()
        let proposal = $('#ProposalId').val()
        p = (grand_total*percentage) / 100
        grand = grand_total - p
        $('#desplay').val(p)

        mydata = {'proposal':proposal,'method':method,'discount':percentage}

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