+function ($, undefined) {
    $(function (){
        var carousel = $(".carousel");

        carousel.carousel();

        $(".carousel-nav span").click(function(e){
            e.preventDefault();
            carousel.carousel($(this).index());
        });

        carousel.on("slid", function() {
            var $this = $(this);
            var index = $this.find(".carousel-inner > .item.active").index();

            $($this.find(".carousel-nav > span")
              .filter(".active").removeClass("active")
              .end()
              .get(index)
             ).addClass("active");
        });

        $(".receiver-addr-toggle", "#checkout-delivery").change(function (e) {
            var el = $(this);
            el.closest("div.product").find(".receiver-addr").toggle(el.val() === "1");
        })

    });

//    var payment_form = $('#payment_form');
//
//    if (payment_form.length) {
//        setTimeout(function() {
//                $('#payment_form').submit();
//            }, 0);
//    }

}(window.jQuery);
