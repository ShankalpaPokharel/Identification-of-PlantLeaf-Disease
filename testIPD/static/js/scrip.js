const video = document.getElementById('video');

const canvas = document.getElementById('canvas');
const captureButton = document.getElementById('capture');
const context = canvas.getContext('2d');

navigator.mediaDevices.getUserMedia({video:true})
.then(stream => {
    video.srcObject = stream;
})

captureButton.addEventListener('click',() =>{
    context.drawImage(video, 0, 0, canvas.width, canvas.height);
    const dataURL = canvas.toDataURL('image/jpeg')
    // console.log(dataURL)
    sendImageData(dataURL);
})

const url = '/predict_image/';

function sendImageData(imageData) {
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    // Send an AJAX request to the Django view with the captured image data
    $.ajax({
        url: url,
        type: 'POST',
        data: {
            'imageData': imageData
        },
        headers: {
            'X-CSRFToken': csrftoken,
        },
        success: function(response) {
            // Update the prediction element on the page with the response data
            $('#prediction').text(response.prediction);
        },
        error: function(xhr, status, error) {
            // Handle any errors that occur during the AJAX request here
            // console.log(error);
        }
    });
}
