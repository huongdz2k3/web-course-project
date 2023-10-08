console.log('Hello World!');
const url = window.location.href;

const quizBox = document.getElementById('quiz-box');
const answerBox = document.getElementById('answer-box');
const scoreBox = document.getElementById('score-box');
const timerBox = document.getElementById('timer-box');
const buttonBox = document.getElementById('button-box'); 
const submitBtn = document.getElementById('submitBtn'); 

function shuffle(sourceArray) {
    for (var i = 0; i < sourceArray.length - 1; i++) {
        var j = i + Math.floor(Math.random() * (sourceArray.length - i));

        var temp = sourceArray[j];
        sourceArray[j] = sourceArray[i];
        sourceArray[i] = temp;
    }
    return sourceArray;
}

const activateTimer = (time) => {
    
    if (time.toString().length < 2) {
        timerBox.innerHTML += `<h2><b>0${time}:00</b></h2>`;
    } else {
        timerBox.innerHTML += `<h2><b>${time}:00</b></h2>`;
    }
    let minutes = time - 1;
    let seconds = 60;
    let displaySeconds;
    let displayMinutes;
    const timer = setInterval(() => {
        seconds--;
        if (seconds < 0) {
            seconds = 59;
            minutes--;
        } 
        if (minutes.toString().length < 2) {
            displayMinutes = `0${minutes}`;
        } else {
            displayMinutes = minutes;
        }
        if (seconds.toString().length < 2) {
            displaySeconds = `0${seconds}`;
        } else {
            displaySeconds = seconds;
        }

        if(submitBtn.disabled == true ){
            timerBox.innerHTML = `<h2><b>${displayMinutes}:${displaySeconds}</b></h2>`;
            
            setTimeout(() => {
                clearInterval(timer);
            }, 500);
        }

        if (seconds == 0 && minutes == 0) {
            timerBox.innerHTML = `<h2><b>00:00</b></h2>`;

            setTimeout(() => {
                clearInterval(timer);
                alert('Time is up');
                sendData();
            }, 500);

            submitBtn.disabled = true;
        }

        timerBox.innerHTML = `<h2><b>${displayMinutes}:${displaySeconds}</b></h2>`;

    }, 1000);
}
let data;
$.ajax({
    type: 'GET',
    url: `${url}/data`,
    success: function (response) {
        
        const data = response.data
        console.log("DATA" + data)
        data.forEach(element => {
            for (const [question, answer] of Object.entries(element)) {
                shuffle(answer)
                quizBox.innerHTML += `
                <hr>
                <div class="card">
                    <div class="card-body" style="background-color: #2D4F93">
                        <h5 class="card-title" style="font-weight: bold; color: white">${question}</h5>
                    </div>
                </div>
                `
                answer.forEach(ele => {
                    if (ele != null) {
                        quizBox.innerHTML += `
                        <div class="card">
                            <div class="card-body form-check" >
                                <input class='ans radio radio-primary form-check-input' type="radio" name="${question}" id="${question}-${answer}" value="${ele}">
                                <label class="form-check-label" for="${question}-${answer}">${ele}</label>
                            </div>
                        </div>
                      `
                        
                    }
                }); 
            }
        });
        window.addEventListener('scroll', () => {
        if (window.scrollY > 20) { // Adjust the threshold as needed
            timerBox.classList.add(stickyClass);
        } else {
            timerBox.classList.remove(stickyClass);
        }
        });
        activateTimer(response.time)
        // back button
        
    },
    error: function (error) {
        console.log(error)
    }
})

const quizForm = document.getElementById('quiz-form')

const csrf = document.getElementsByName('csrfmiddlewaretoken')

// $(document).ready(function () {

//     $("#quiz-form").submit(function (e) {

//         //stop submitting the form to see the disabled button effect
//         e.preventDefault();

//         //disable the submit button
//         $("#submitBtn").attr("disabled", true);

//         return true;

//     });
// });

const sendData = () => {
    const elements = [...document.getElementsByClassName('ans')]

    const data = {}
    data['csrfmiddlewaretoken'] = csrf[0].value
    elements.forEach(el => {
        if (el.checked) {
            data[el.name] = el.value
        } else {
            if (!data[el.name]) {
                data[el.name] = null
            }
        }
    })

    $.ajax({
        type: 'POST',
        url: `${url}/save`,
        data: data,
        success: function (response) {
            
            const results = response.results
            console.log("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA: ", results)
            quizForm.classList.add('not-visible')
             $(document).ready(function () {

        // $("#formABC").submit(function (e) {

        //     //stop submitting the form to see the disabled button effect
        //     e.preventDefault();

        //     //disable the submit button
        //     $("#btnSubmit").attr("disabled", true);

        //     //disable a normal button
        //     $("#btnTest").attr("disabled", true);

        //     return true;

        // });
        });

            scoreBox.innerHTML = `${response.passed ? 'Congratulation!' : 'Sorry you`re failed'} | Your score is ${response.score}`

            results.forEach(res => {

                const resDiv = document.createElement('div')
                for (const [question, resp] of Object.entries(res)) {

                    resDiv.innerHTML += question
                    const cls = ['container', 'p-3','text-light', 'h3']
                    resDiv.classList.add(...cls)
                    resDiv.style.color = "#34495E"
                    if (Object.keys(resp).includes('not_answered') ) {
                        resDiv.innerHTML += ' Not answered'
                        resDiv.classList.add('bg-danger')
                    }
                    else {
                        const answer = resp['answered']
                        const correct = resp['correct_answer']

                        if (answer == correct) {
                            resDiv.classList.add('bg-success')
                            resDiv.innerHTML += ` Your answered: ${answer}`
                        } else {
                            resDiv.classList.add('bg-danger')
                            resDiv.innerHTML += ` Your answered: ${answer}`
                        }
                    }
                }
                answerBox.append(resDiv);
                const url_temp = window.location.href;
                const url_course = url_temp.split("/");
                buttonBox.innerHTML = `<a href="${url_course.slice(0,-1).join("/")}" class="btn btn-primary">Back</a>`
                // after 10 seconds redirect to home page
            });
        },
        error: function (error) {
            console.log(error);
        }
    })
}

quizForm.addEventListener('submit', e => {
    e.preventDefault();
    if (confirm("Are you sure to submit")) {
        submitBtn.value = "Submited";
        submitBtn.disabled = true;
        sendData();
    } else {
      return false;
    } 
})

// Disable navigation through the back button
history.pushState(null, null, location.href);
window.onpopstate = function () {
    history.go(1);
};

window.addEventListener('beforeunload', function (e) {
    // Display a confirmation message
    e.preventDefault();
    e.returnValue = '';
});