$(document).ready(function(){
    // https secure site when live
    var paymentForm = $(".stripe-payment-form")
    var stripeToken = paymentForm.attr("data-token")
    var stripeNextUrl = paymentForm.attr("data-next-url")
    var stripeBtnTitle = paymentForm.attr("data-btn-title") || "Add card"
    var stripeTemplate = $.templates("#stripeTemplate")
    var stripeTemplateDataContext = {
      publish_key: stripeToken,
      next_url: stripeNextUrl,
      btn_title: data-btn-title
    }
    var stripeTemplateHtml = stripeTemplate.render(stripeTemplateDataContext)
    stripeFormModule.html(stripeTemplateHtml)
    if (paymentForm.length > 1){
        alert("Only one payment form is allowed per page")
        paymentForm.css('display', 'none')
    }
    else if (paymentForm.length == 1) {

    var pubKey = paymentForm.attr('data-token')
    var nextUrl = paymentFrom.attr('data-next-url')

    // Create a Stripe client.
    var stripe = Stripe(pubKey);

    // Create an instance of Elements.
    var elements = stripe.elements();

    // Custom styling can be passed to options when creating an Element.
    // (Note that this demo uses a wider set of styles than the guide below.)
    var style = {
      base: {
        color: '#32325d',
        fontFamily: '"Helvetica Neue", Helvetica, sans-serif',
        fontSmoothing: 'antialiased',
        fontSize: '16px',
        '::placeholder': {
          color: '#aab7c4'
        }
      },
      invalid: {
        color: '#fa755a',
        iconColor: '#fa755a'
      }
    };

    // Create an instance of the card Element.
    var card = elements.create('card', {style: style});

    // Add an instance of the card Element into the `card-element` <div>.
    card.mount('#card-element');

    // Handle real-time validation errors from the card Element.
    card.addEventListener('change', function(event) {
      var displayError = document.getElementById('card-errors');
      if (event.error) {
        displayError.textContent = event.error.message;
      } else {
        displayError.textContent = '';
      }
    });

    // Handle form submission.
    var form = document.getElementById('payment-form');
    form.addEventListener('submit', function(event) {
      event.preventDefault();

      stripe.createToken(card).then(function(result) {
        if (result.error) {
          // Inform the user if there was an error.
          var errorElement = document.getElementById('card-errors');
          errorElement.textContent = result.error.message;
        } else {
          // Send the token to your server.
          stripeTokenHandler(nextUrl, result.token);
        }
      });
    });

    function redirectToNext(nextPath, timeOffset){
    if (nextPath){
    setTimeout(function(){
      window,location.href = nextPath
    },timeOffset)
    }
    }

    // Submit the form with the token ID.
    function stripeTokenHandler(nextUrl, token) {
      // Insert the token ID into the form so it gets submitted to the server
      var paymentMethodEndpoint = '/billing/payment-method/create/'
      var data ={
        'token': token.id
      }
      $.ajax({
        data: data,
        url: paymentMethodEndpoint,
        method: "POST",
        success: function(data){
            var succesMsg = data.message || "Success! Your card was added."
            card.clear()
            if (nextUrl{
              succesMsg = succesMsg + "<br/><i class='fa fa-spin fa-spinner'></i> Redirecting ..."
            }
            if ($.alert){
              $.alert(succesMsg)
            }else {
              alert(succesMsg)
            }
            redirectToNext(nextUrl, 1500)
        },
        error: function(error){
            console.log(error)
        },
      })
      var form = document.getElementById('payment-form');
      var hiddenInput = document.createElement('input');
      hiddenInput.setAttribute('type', 'hidden');
      hiddenInput.setAttribute('name', 'stripeToken');
      hiddenInput.setAttribute('value', token.id);
      form.appendChild(hiddenInput);

      // Submit the form
      // form.submit();
    }
    }
})


