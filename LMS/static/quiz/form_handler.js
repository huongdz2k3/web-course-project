const submitBtn = document.getElementById('submitBtn')

{/* <form method="POST" action="..." onsubmit="return checkForm(this);">
  <p>First Name: <input type="text" required name="firstname"></p>
  <p>Last Name: <input type="text" required name="lastname"></p>
  <p><input type="submit" name="myButton">
    <input type="button" value="Reset" onclick="resetForm(this.form);"></p>
</form> */}

{/* <form id="quiz-form" form="mt-3 mb-3">
        {% csrf_token %}
        <div id ='quiz-box'>
        </div>
        <div class="text-center" >
            <button id="submitBtn" name="submitBtn" type="submit" class="btn btn-primary mt-3" >Submit</button>
        </div>
</form> */}

var form_being_submitted = false; /* global variable */

var checkForm = function (form) {

    // if (form_being_submitted) {
    //     alert("The form is being submitted, please wait a moment...");
    //     form.myButton.disabled = true;
    //     return false;
    // }

    // if (form.firstname.value == "") {
    //     alert("Please enter your first and last names");
    //     form.firstname.focus();
    //     return false;
    // }
    // if (form.lastname.value == "") {
    //     alert("Please enter your first and last names");
    //     form.lastname.focus();
    //     return false;
    // }
    form.submitBtn.value = 'Submited.';
    form_being_submitted = true;
    return true; 
};

var resetForm = function (form) {
    form.submitBtn.disabled = false;
    form.submitBtn.value = "Submit";
    form_being_submitted = false;
};

