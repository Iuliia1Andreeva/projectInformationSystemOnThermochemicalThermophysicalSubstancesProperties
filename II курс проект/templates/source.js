let first_form = document.getElementById("sign_in_form");
let first_button = document.getElementById("btn_sign_up");
let second_form = document.getElementById("sign_up_form");
let second_button = document.getElementById("btn_sign_in")



first_button.onclick = function() {
     first_form.style.display = "none";
     second_form.style.display = "block";
};

second_button.onclick = function() {
    second_form.style.display = "none";
    first_form.style.display = "block";
};



