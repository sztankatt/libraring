 $(document).ready(function(){
    var $container = $('#genre_books_all');

    if($container.length != 0){
        
        $container.masonry();
        $container.masonry('destroy');
        
        $container.masonry({
            gutter: '.book-gutter-sizer',

            columnWidth: '.book-grid-sizer',
            itemSelector: '.book-container',
        });
        
        $container.imagesLoaded(function(){
            $container.masonry();
        });

    }

    $(".left-nav-footer button").click(function(){
        $this = $(this);
        if($this.hasClass('normal')){
            $this.removeClass('normal').addClass('slided');
            $(".left-side .left-nav-body").fadeOut("fast");
            $this.children('.text').fadeOut();

            $this.removeClass('btn-block').animate({
                width:"30px",
                padding:"6px 6px"
            }).children('i').css({'margin':'0px'}).removeClass('fa-minus').addClass('fa-plus');

            $(".home-container .left-side").animate({
                width: "50px"
            }, 500);

            $(".home-container .right-side").animate({
               marginLeft:"50px"
            }, 500, function(){
                if($container.length != 0){
                    $container.masonry();
                }
            });
        }
        else{
            $this.removeClass('slided').addClass('normal');
            $this.addClass('btn-block').animate({
                width:"180px",
                padding:"6px 12px"
            }).children('i').css({'margin':'5px'}).removeClass('fa-plus').addClass('fa-minus');

            $(".home-container .left-side").animate({
                width: "200px"
            }, 500);

            $(".home-container .right-side").animate({
               marginLeft:"200px"
            }, 500, function(){
                if($container.length != 0){
                    $container.masonry();
                }
            });
            $(".left-side .left-nav-body").fadeIn("fast");
            $this.children('.text').fadeIn("fast");
        }

        $('.main-menu-navbar .toggle-collapse-menu').click(function(){
            $('ul.main-menu-left').slideToggle('fast');
        });

        $(window).resize(function(){
            if(window.innerWidth > 500){
                $('ul.main-menu-left').show();
            }
            else{
                $('ul.main-menu-left').hide();
            }
        });

    });


/*
    New offer form .js
 */
 validators_feedback_icons = {
        valid: 'glyphicon glyphicon-ok',
        invalid: 'glyphicon glyphicon-remove',
        validating: 'glyphicon glyphicon-refresh'
    };

    /*$('.usr-book-status-body form').bootstrapValidator({
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
    });   */

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
        var $made_by = $('#id_made_by').val();

        var offered_price = $('#id_offered_price').val();

        $form.ajaxSubmit(function(data){
            var inserted = false;

            var element_num = 0;

            toastr.success('Offer made!');
            $('.book-offer-previous .book-offer-previous-element').each(function(i){
                if ($(this).attr('data-offer-made-by') == $made_by){
                    $(this).remove();
                }
            });

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

    $('#delete_offer_form').ajaxForm(function(data){
        $('.modal').modal('hide');
    });
});