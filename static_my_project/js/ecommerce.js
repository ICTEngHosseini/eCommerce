$(document).ready(function(){
    // Contact form handler
    var contactForm = $(".contact-form")
    var contactFormMethod = contactForm.attr("method")
    var contactFormEndpoint = contactForm.attr("action") // /abc/
    contactForm.submit(function(event){
        event.preventDefault()
        var contactFormData = contactForm.serialize()
        $.ajax({
            method: contactFormMethod,
            url: contactFormEndpoint,
            data: contactFormData,
            success: function(data){
                contactForm[0].reset()
                $.alert({
                    title: 'Success!',
                    content: data.message,
                    theme: 'dark',
                })
            },
            error: function(error){
                $.alert({
                    title: 'Alert!',
                    content: 'Simple alert!',
                    theme: 'dark',
                })
            }
        })
    })

    // Auto Search
    var searchForm = $(".search-form")
    var searchInput = searchForm.find("[name='q']") // input name='q'
    var typingTimer;
    var typingInterval = 500 // 0.5 seconds
    var searchBtn = searchForm.find("[type='submit']")
    searchInput.keyup(function(event){
        // key released
        clearTimeout(typingTimer)
        typingTimer = setTimeout(perfomSearch, typingInterval)
    })
    searchInput.keydown(function(event){
        // key pressed
        clearTimeout(typingTimer)
    })
    function displaySearching(){
        searchBtn.addClass("disabled")
        searchBtn.html("<i class='fa fa-spin fa-spinner'></i> Searching...")
    }
    function perfomSearch(){
        displaySearching()
        var query = searchInput.val()
        setTimeout(function(){
            window.location.href='/search/?q=' + query
        }, 1000)
    }

    // Cart + Add Products
    var productForm = $(".form-product-ajax") // #form-product-ajax

    productForm.submit(function(event){
        event.preventDefault();
        var thisForm = $(this)
        var actionEndpoint = thisForm.attr("action"); // API Endpoint
        var httpMethod = thisForm.attr("method");
        var formData = thisForm.serialize();

        $.ajax({
            url: actionEndpoint,
            method: httpMethod,
            data: formData,
            success: function(data){
                // console.log(data)
                var submitSpan = thisForm.find(".submit-span")
                if (data.added){
                    submitSpan.html("<button class='btn btn-warning'><i class='fas fa-shopping-cart'></i></button>")
                } else {
                    submitSpan.html("<button class='btn btn-dark'><i class='fas fa-cart-plus'></i></button>")
                }
                var navbarCount = $(".navbar-cart-count")
                navbarCount.text(data.cartItemCount)
                var currentPath = window.location.href

                if (currentPath.indexOf("cart") != -1){
                    refreshCart()
                }
            },
            error:function(errorData){
                $.alert({
                    title: 'Alert!',
                    content: 'Simple alert!',
                    theme: 'dark',
                })
            }
        })
    })

    function refreshCart(){
        var cartTable = $(".cart-table")
        var cartBody = cartTable.find(".cart-body")
        // cartBody.html("")
        var productRows = cartBody.find(".cart-product")
        var currentUrl = window.location.href

        var refreshCartUrl = '/api/carts/';
        var refreshCartMethod = "GET";
        var data = {};
        $.ajax({
            url: refreshCartUrl,
            method: refreshCartMethod,
            data: data,
            success: function(data){
                // console.log(data)
                // console.log("success")
                var hiddenCartItemRemoveForm = $(".cart-item-remove-form")
                if (data.products.length > 0){

                    productRows.html(" ")
                    i = data.products.length
                    $.each(data.products, function(index, value){
                        // console.log("you r here")
                        var newCartItemRemove = hiddenCartItemRemoveForm.clone()
                        newCartItemRemove.css("display", "block")
                        // newCartItemRemove.removeClass("hidden-class")
                        newCartItemRemove.find(".cart-item-product-id").val(value.id)
                        cartBody.prepend("<tr><th scope=\"row\">" + i + "</th><td><a href='" + value.url + "'>" + value.name + "</a>" +  newCartItemRemove.html() + "</td><td>" + value.price + "</td></tr>")
                        i --
                        // console.log(newCartItemRemove)
                    })
                    cartBody.find(".cart-subtotal").text(data.subtotal)
                    cartBody.find(".cart-total").text(data.total)
                } else{
                    window.location.href = currentUrl
                }
            },
            error: function(errorData){
                $.alert({
                    title: 'Alert!',
                    content: 'Simple alert!',
                    theme: 'dark',
                })
            }
        })
    }
})