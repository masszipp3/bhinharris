/*
Template Name: Foodmart - Food & Grocery Delivery Mobile Template
Author: Askbootstrap
Author URI: https://themeforest.net/user/askbootstrap
Version: 0.1
*/

/*
- Sidebar
- Coupons
- Top Picks - Homepage
- All Categories - Homepage
- Product Detail
*/

// (function ($) {
//     "use strict"; // Start of use strict
    $(document).ready(function () {

        $.ajaxSetup({
            headers: {
                "X-CSRFToken": $('[name=csrfmiddlewaretoken]').val()
            }
        })
        
        // Cart Item
        $('.cminus').click(function () {
            var input = $(this).parent().find('.box');  
            var main=$(this).parent().parent()
            console.log(main)
            var productid = input.attr('ppid')
            var url = input.siblings('.cplus').data('url')
            $.ajax({
                type: 'POST',
                url: url,
                data: {
                    'productid': productid,
                    'from':true

                },
                success: function (response) {
                    data=response.data
                    var count = parseInt(input.val()) - 1;
                    count = count < 1 ? 0 : count;
                    if(count==0){
                        main.remove()
                    }
                    input.val(count);
                    discountamount=response.dicountedprice
                    subtotal=input.parent().siblings('.subtotal')
                    var total=response.finaltotal
                    // var vat= total*0.05
                    // total=total+vat
                    // vat=vat.toFixed(2)
                    total=total.toFixed(2)
                    subtotal.html('ر.ع '+response.subtotal  )
                    $('#subtotals').html('OMR '+total)
                    $('#grandtotal').html('OMR '+ response.total)
                    $('#finaltotal').html('OMR '+response.total)
                    $('#downtotal').html('OMR '+total)
                    // $('#vat').html('OMR '+vat)
                    // $('#finalvat').html('OMR '+vat)
                    $('#finalamount').html('OMR '+total)
                    var discount=response.discountfinal-response.finaltotal
                    console.log(discount)
                    $('#finaldiscount').html('OMR '+ discount.toFixed(2))
                    $('#discountt').html('OMR '+discountamount)


                    // total='Rs ' + response.total
                    // count=response.count + ' items in cart'
                    // $('#counts').html(count)
                    // $('#total').html(total)
                    // var currentCount = parseInt(productCountInput.val());
                    // console.log(productCountInput.val())
                    // if (currentCount > 0) {
                    //   productCountInput.val(currentCount - 1);
                    //   console.log(productCountInput.val())
                    // }
                    // if(productCountInput.val()<1) {
                    //     addButton.show(); 
                    //     productCountDiv.addClass("none")
                    //   }
                    
                    // console.log(data)
                    // addButton.hide();
                    // productCountDiv.removeClass("none").show();
                    // productCountInput.val("1");
                    // $('#hoi').empty();
                    // $('#hoi').append($('<option>').text('Select a Staff').attr('value', ''));
                    // for (d in data) {
                    //     console.log(d)
                    //     $('#hoi').append($('<option>').text(data[d].name).attr('value',data[d].id));
                    // }
                },
                error: function (xhr, status, error) {
                    console.error(xhr.responseText);
                }
            });
            


        });
        $('.cplus').click(function () {
            var input = $(this).parent().find('.box');
            var productid = input.attr('ppid')
            var url = input.data('url')
            console.log(productid,url)

            $.ajax({
                type: 'POST',
                url: url,
                data: {
                    'productid': productid,
                    'from':true
                },
                success: function (response) {
                    data = response.data
                    console.log(data)
                    var total=response.finaltotal
                    // var vat= total*0.05
                    // total=total+vat
                    // vat=vat.toFixed(2)
                    total=total.toFixed(2)
                    discountamount=response.dicountedprice

                    
                    
                    subtotal=input.parent().siblings('.subtotal')
                    subtotal.html('ر.ع   '+response.subtotal)
                    $('#subtotals').html('OMR '+total)
                    $('#grandtotal').html('OMR '+response.total)
                    $('#finaltotal').html('OMR '+response.total)
                    $('#downtotal').html('OMR '+total)
                    // $('#vat').html('OMR '+vat)
                    // $('#finalvat').html('OMR '+vat)
                    $('#finalamount').html('OMR '+total)
                    $('#discountt').html('OMR '+discountamount)
                    var discount=response.total-response.discountfinal
                    console.log(discount)
                    $('#finaldiscount').html('OMR '+discount.toFixed(2))

                    input.val(parseInt(input.val()) + 1);
                    // count=response.count + ' items in cart'
                    // $('#counts').html(count)
                    // $('#total').html(total)

                    // console.log(count)
                    // console.log(total)
                    // var currentCount = parseInt(productCountInput.val());
                    // productCountInput.val(currentCount + 1); 

                    // console.log(data)
                    // addButton.hide();
                    // productCountDiv.removeClass("none").show();
                    // productCountInput.val("1");
                    // $('#hoi').empty();
                    // $('#hoi').append($('<option>').text('Select a Staff').attr('value', ''));
                    // for (d in data) {
                    //     console.log(d)
                    //     $('#hoi').append($('<option>').text(data[d].name).attr('value',data[d].id));
                    // }
                },
                error: function (xhr, status, error) {
                    console.error(xhr.responseText);
                }
            });
            


        });

    });

    // Sidebar
    var $main_nav = $('#main-nav');
    var $toggle = $('.toggle');
    var defaultOptions = {
        disableAt: false,
        customToggle: $toggle,
        levelSpacing: 40,
        navTitle: 'App',
        levelTitles: true,
        levelTitleAsBack: true,
        pushContent: '#container',
        insertClose: 2
    };
    var Nav = $main_nav.hcOffcanvasNav(defaultOptions);

    // Coupons
    // $('.coupons').slick({
    //     infinite: false,
    //     arrows: false,
    //     autoplay: true,
    //     slidesToShow: 1.3,
    //     slidesToScroll: 1,
    // });

    // // Top Picks - Homepage
    // $('.top-picks').slick({
    //     infinite: false,
    //     arrows: false,
    //     autoplay: true,
    //     slidesToShow: 2.3,
    //     slidesToScroll: 1,
    // });

    // // All Categories - Homepage
    // $('.all-cate').slick({
    //     infinite: false,
    //     arrows: false,
    //     autoplay: true,
    //     slidesToShow: 4.5,
    //     slidesToScroll: 4,
    // });

    // // Product Detail
    // $('.product-slider').slick({
    //     arrows: false,
    //     autoplay: true,
    //     infinite: false,
    //     dots: true,
    // });



// })(jQuery);