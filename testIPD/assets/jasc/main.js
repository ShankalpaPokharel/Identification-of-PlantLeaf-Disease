
{% extends 'camera.html' %}
const video = document.getElementById('video');
const captureButton = document.getElementById('capture');
const uploadForm = document.getElementById('upload-form');
const imageDataInput = document.getElementById('image-data');



console.log("Detecting main.js")

// Get access to the user's camera
navigator.mediaDevices.getUserMedia({ video: true })
  .then(stream => {
    // Display the camera stream in the video element
    video.srcObject = stream;
  })
  .catch(error => {
    console.error('Error accessing the camera:', error);
  });

// Capture an image from the camera
captureButton.addEventListener('click', () => {
  const canvas = document.createElement('canvas');
  canvas.width = video.videoWidth;
  canvas.height = video.videoHeight;
  canvas.getContext('2d').drawImage(video, 0, 0);
  
  // Convert the canvas image to a data URL
const imageData = canvas.toDataURL();
imageDataInput.value = imageData;
});

// Upload the image data to the server
uploadForm.addEventListener('submit', event => {
event.preventDefault();
const formData = new FormData(uploadForm);
fetch(uploadForm.action, {
method: 'POST',
body: formData,
})
.then(response => {
console.log('Photo uploaded:', response);
})
.catch(error => {
console.error('Error uploading photo:', error);
});
});
