document.addEventListener("DOMContentLoaded", function () {

    const chartElement = document.getElementById("taskChart");

    if (chartElement) {

        const completed = parseInt(chartElement.dataset.completed);
        const pending = parseInt(chartElement.dataset.pending);

        new Chart(chartElement, {

            type: "pie",

            data: {

                labels: ["Completed", "Pending"],

                datasets: [{
                    data: [completed, pending],

                    backgroundColor: [
                        "#22c55e",
                        "#ef4444"
                    ],

                    borderWidth: 1
                }]
            },

            options: {

                responsive: true,

                plugins: {

                    legend: {
                        position: "bottom"
                    }
                }
            }
        });
    }

});

// ---------------- Pomodoro Timer ----------------

let time = 25 * 60;
let timerInterval = null;
let sessions = 0;

const timer = document.getElementById("timer");
const sessionText = document.getElementById("sessions");

function updateTimer(){

    const minutes = Math.floor(time / 60);
    const seconds = time % 60;

    timer.textContent =
        String(minutes).padStart(2,"0") + ":" +
        String(seconds).padStart(2,"0");

}

document.getElementById("startBtn").onclick = function(){

    if(timerInterval) return;

    timerInterval = setInterval(function(){

        time--;

        updateTimer();

        if(time <= 0){

            clearInterval(timerInterval);

            timerInterval = null;

            alert("Pomodoro Complete!");

            sessions++;

            sessionText.textContent = sessions;

            time = 25 * 60;

            updateTimer();

        }

    },1000);

};

document.getElementById("pauseBtn").onclick = function(){

    clearInterval(timerInterval);

    timerInterval = null;

};

document.getElementById("resetBtn").onclick = function(){

    clearInterval(timerInterval);

    timerInterval = null;

    time = 25 * 60;

    updateTimer();

};

updateTimer();