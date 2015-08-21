$(document).ready(function(){
	 validators_feedback_icons = {
        valid: 'glyphicon glyphicon-ok',
        invalid: 'glyphicon glyphicon-remove',
        validating: 'glyphicon glyphicon-refresh'
    };

    $('#brainstorm_form').bootstrapValidator({
    	feedbackIcons: validators_feedback_icons,
    	fields:{
    		name:{
	    		validators: {
		    		notEmpty: {
		    			message: 'This field is required.'
		    		}
		    	}
    		},
    		email: {
    			validators: {
		    		notEmpty: {
		    			message: 'This field is required.'
		    		}
		    	}
    		},
    		comment: {
    			validators: {
		    		notEmpty: {
		    			message: 'This field is required.'
		    		}
		    	}
		    }
    	}
    });

    $('.before-login-book-container').slick({
        //prevArrow: $('.index-page-content .slider-navigation.fa-arrow-left'),
        //nextArrow: $('.index-page-content .slider-navigation.fa-arrow-right'),
        arrows: false,
        infinite: true,
        autoplay: true,
        autoplaySpeed: 2000,
        slidesToShow: 3,
        slidesToScroll: 3,
        responsive:[
            {
                breakpoint: 1400, 
                settings:{       
                    slidesToShow: 2,
                    slidesToScroll: 2,
                    infinite: true
                }
            },
            {
                breakpoint: 768,
                settings:{
                    slidesToScroll: 1,
                    slidesToShow: 1,
                    infinite: true
                }
            }
        ]
    });
});