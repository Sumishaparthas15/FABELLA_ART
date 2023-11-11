document.addEventListener('DOMContentLoaded', function() {
    var payButton = document.querySelector('.paywithrazorpay');

    payButton.addEventListener('click', function(event) {
        event.preventDefault();

        var selects = document.querySelector("[name='addressId']").value;

        if (selects === "") {
            swal("Alert", "Address field is needed", "error");
            return false;
        } else {
            fetch('/proceedtopay')
                .then(function(response) {
                    if (!response.ok) {
                        throw new Error('Network response was not ok');
                    }
                    return response.json();
                })
                .then(function(data) {
                    var options = {
                        key: 'rzp_test_d5VCv4MOwkIpcU',
                        amount: data.total * 100,
                        currency: 'INR',
                        name: 'Fabella Art',
                        description: 'Thank you for Placing an order ',
                        image: 'https://static-00.iconduck.com/assets.00/bill-payment-icon-2048x2048-vpew78n5.png',
                        handler: function(responseb) {
                            // Assuming you have the order_id and total_amount in the response
                            var order_id = responseb.order_id;
                            var total_amount = data.total;

                            createRazorpayOrder(order_id, total_amount);
                        },
                        prefill: {
                            name: 'SUMISHA',
                            email: 'sumishasudha392@gmail.com',
                            contact: '9037235334'
                        },
                        notes: {
                            address: 'Razorpay Corporate Office'
                        },
                        theme: {
                            color: '#D19C97'
                        }
                    };

                    var rzp1 = new Razorpay(options);
                    rzp1.open();
                })
                .catch(function(error) {
                    console.error('Error:', error);
                });
        }
    });
});
