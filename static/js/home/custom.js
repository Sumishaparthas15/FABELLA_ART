// custom.js

$(document).ready(function () {
    // Add to Cart button click event
    $("#add-to-cart-btn").click(function () {
        // Assuming product is defined in your template context
        let product_id = "{{ product.id }}";

        $.ajax({
            type: "POST",
            url: "{% url 'add_to_cart' 123 %}".replace(123, product_id),  // Replace 123 with any placeholder
            data: {
                csrfmiddlewaretoken: "{{ csrf_token }}",
                quantity: 1,
            },
            dataType: "json",
            success: function (response) {
                // Log the response in the console
                console.log(response);

                // Check if the product was added successfully
                if (response.success) {
                    alert('Product added to cart');
                } else {
                    alert('Error adding product to cart: ' + response.message);
                }
            },
            error: function (xhr, errmsg, err) {
                console.log(xhr.status + ": " + xhr.responseText);
                alert('Error adding product to cart');
            }
        });
    });
});

