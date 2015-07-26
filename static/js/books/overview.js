$(document).ready(function(){
    validators_feedback_icons = {
        valid: 'glyphicon glyphicon-ok',
        invalid: 'glyphicon glyphicon-remove',
        validating: 'glyphicon glyphicon-refresh'
    };

    $('#book_offer_form').bootstrapValidator({
    	feedbackIcons : validators_feedback_icons,
    	fields: {
    		offered_price:{
    			validators:{
    				notEmpty:{
    					message: 'This field is required.'
    				}
    			}
    		}
    	}
    })
    .on('success.form.bv', function(e){
    	e.preventDefault();

    	var $form = $(e.target);


    	var offered_price = $('#id_offered_price').val();

    	$form.ajaxSubmit(function(data){
    		var inserted = false;

            var element_num = 0;

    		toastr.success('Offer made!');
			$('.book-offer-previous .book-offer-previous-element').each(function(i){
				$this = $(this);
				var val = $this.attr('data-offered-price');
                element_num = element_num + 1;

				if (offered_price >= val){
					$this.before(data);
					inserted = true;
					return false;
				}
			});

            if(element_num == 0){
                $('.book-no-offer').remove();
            }

			if (!inserted){
				$('.book-offer-previous').append(data);
			}
    	});

    	$form.data('bootstrapValidator').resetForm();
    	$('#id_offered_price').val('');
    });



});