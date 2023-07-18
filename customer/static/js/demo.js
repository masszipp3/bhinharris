/*
Template Name: Foodmart - Food & Grocery Delivery Mobile Template
Author: Askbootstrap
Author URI: https://themeforest.net/user/askbootstrap
Version: 0.1
*/

/*
- Demo Slider
*/

(function ($) {
    "use strict"; // Start of use strict

    // Demo Slider
    $('.demo-slider').slick({
        infinite: false,
        arrows: true,
        autoplay: true,
        slidesToShow: 3.5,
        slidesToScroll: 1,
    });

})(jQuery);

$(document).ready(function(){
    $('#screen').removeClass('hidden').addClass('phone-screen')  
    $('#truck').delay(2300).hide(0)
    $('#description').delay(2300).show(0)

    $('#description').animate({left: "5%"}, 1000);
})