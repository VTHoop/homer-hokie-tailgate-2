$(document).ready(function() {

    $('.js--game-details').waypoint(function(direction) {
       if (direction == 'down') {
           $('nav').addClass('sticky');
       } else {
           $('nav').removeClass('sticky');
       }
    },{
        offset: '21%;'
    });

    
    /*scroll on button */
    $('.js--scroll-to-menu').click(function () {
       $('html, body').animate({scrollTop: $('.js--section-menu').offset().top -100}, 1000); 
    });
    
    $('.js--scroll-to-attendance').click(function () {
       $('html, body').animate({scrollTop: $('.js--section-attendance').offset().top -100}, 1000); 
    });
    
    $('.js--scroll-to-preview').click(function () {
       $('html, body').animate({scrollTop: $('.js--section-preview').offset().top -100}, 1000); 
    });
    
    $('.js--scroll-to-tickets').click(function () {
       $('html, body').animate({scrollTop: $('.js--section-tickets').offset().top -100}, 1000); 
    });

    $("#dashboardScores input[type='text']").on("click", function () {
        $(this).select();
    });

    
});