<script>
    function handlePaymentSelection() {
        var paymentMethod = document.querySelector('input[name="payment"]:checked').value;

        if (paymentMethod === "razorpay") {
            document.getElementById("rzp-button1").style.display = "block";
            document.getElementById("place-order-button").style.display = "none";
        } else {
            document.getElementById("rzp-button1").style.display = "none";
            document.getElementById("place-order-button").style.display = "block";
        }
    }
</script>
