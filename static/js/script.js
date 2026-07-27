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