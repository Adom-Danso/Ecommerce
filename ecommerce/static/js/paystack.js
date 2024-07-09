document.getElementById('pay-button').addEventListener('click', payWithPaystack);

function generateRandomReference() {
      const randomNumber = Math.random().toString(36).substr(2, 9); // Generate random number in base36 format
      const timestamp = Date.now().toString(36); // Convert current timestamp to base36 format
      return `${randomNumber}${timestamp}`;
  }

const randomReference = generateRandomReference();

function payWithPaystack(e) {
    e.preventDefault();  // Prevent the form from submitting 

    let handler = PaystackPop.setup({
        key: 'pk_live_44145ccc7c2c714194e4c287f6f23ed89aabd7bd', // Replace with your public key
        email: document.getElementById("email-address").value,
        amount: document.getElementById("amount").value * 100,
        currency: 'GHS',
        ref: randomReference,
        onClose: function(){
            alert('Transaction was not completed, window closed.');
        },
        callback: function(response){
            document.getElementById('paymentForm').submit();  // Submit the form with the payment reference
        }
    });

    handler.openIframe();
}

document.getElementById('pay-button').addEventListener('click', send_ref);


function send_ref() {
    const data = {
        ref: randomReference,
    };
    
    fetch('/submit_ref_data', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data)
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json(); // Parse the JSON response
    })
    .then(data => {
        console.log('Success:', data); // Handle the successful response
        // Update UI or handle success scenario
    })
    .catch(error => {
        console.error('Error:', error); // Handle errors
        // Update UI or handle error scenario
    });
}

send_ref();