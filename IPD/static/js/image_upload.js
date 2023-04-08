let dropzone = document.querySelector('.dropzone');
let fileInput = document.querySelector('#fileInput');
let previewImage = document.querySelector('#previewImage');
let deleteIcon = document.querySelector('#deleteIcon');
let submitBtn = document.querySelector('#submitBtn');

function handleFileSelect(event) {
  let file = event.target.files[0];
  if (file.type.startsWith('image/')) {
    let reader = new FileReader();
    reader.onload = (e) => {
      previewImage.src = e.target.result;
      previewImage.style.display = 'block';
      deleteIcon.style.display = 'inline-block';
      dropzone.classList.remove('dragover');
      dropzone.classList.add('disabled');
      fileInput.classList.add('disabled');
      submitBtn.disabled = false;
    

    }
    reader.readAsDataURL(file);
  } else {
    alert('Please choose an image file.');
  }
}

fileInput.addEventListener('change', handleFileSelect);

dropzone.addEventListener('dragover', (e) => {
  e.preventDefault();
  dropzone.classList.add('dragover');
});

dropzone.addEventListener('dragleave', () => {
  dropzone.classList.remove('dragover');
});

dropzone.addEventListener('drop', (e) => {
  e.preventDefault();
  let file = e.dataTransfer.files[0];
  if (file.type.startsWith('image/')) {
    let reader = new FileReader();
    reader.onload = (e) => {
      previewImage.src = e.target.result;
      previewImage.style.display = 'block';
      deleteIcon.style.display = 'inline-block';
      dropzone.classList.remove('dragover');
      dropzone.classList.add('disabled');
      fileInput.classList.add('disabled');
      submitBtn.disabled = false;
    
    }
    reader.readAsDataURL(file);
  } else {
    alert('Please choose an image file.');
  }
});

deleteIcon.addEventListener('click', () => {
  previewImage.style.display = 'none';
  deleteIcon.style.display = 'none';
  fileInput.value = '';
  submitBtn.disabled = true;
  dropzone.classList.remove('disabled');
  fileInput.classList.remove('disabled');
});

