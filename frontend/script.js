// Get the loading icon element
const loadingIcon = document.getElementById('loading-icon');

// Show the loading icon
loadingIcon.style.display = 'block';

const textField = document.getElementById('outputText');
const imageField = document.getElementById('outputImage');
const generatorButton = document.getElementById('generatorButton');


// Add click event listener to the clear button
generatorButton.addEventListener('click', function() {
  // Clear the value of the text field
  textField.innerText = "LOADING...";
  imageField.src = " ";
});

document.getElementById("inputForm").addEventListener("submit", function(event) {
    event.preventDefault(); // Prevent form submission
    var input = document.getElementById("input").value;
    console.log("post")
    // // Update the output text
    // document.getElementById("outputText").innerText = "LOADING...";
      
    // // Update the output image
    // document.getElementById("outputImage").src = "";
    // Make a request to the backend
    fetch("http://localhost:5000/run-script", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({input: input})
    })
    .then(response => response.json())
    .then(data => {
      // Update the output text
      document.getElementById("outputText").innerHTML = data.outputText;
      
      // Update the output image
      document.getElementById("outputImage").src = data.outputImage;
      
      // Hide the loading icon
      loadingIcon.style.display = 'none';
    })
    .catch(error => {
      console.error("Error:", error);
      
      // Hide the loading icon
      loadingIcon.style.display = 'none';
    });
  });