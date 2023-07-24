document.getElementById("myInput").value = "+968 - "

document.getElementById("myInput").addEventListener("focus", function () {
   this.value = "+968 - ";
   // Replace "Default text" with the desired text you want to show on focus
});
document.getElementById("myInput").addEventListener("blur", function () {
    if(this.value=='+968 - ') 
        this.value = "";
});
function updatePhoneNumber(input) {
   if (!input.value.startsWith("+968 - ")) {
      input.value = "+968 - "
   }
}

function validateLogin(event) {
    var input= document.getElementById('myInput').value
    if(input.length < 15){
        document.getElementById('error').innerHTML='Enter a Valid Mobile Number..!'
        event.preventDefault();

    }
    
   
}