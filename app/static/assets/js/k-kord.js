function plotArmGraphs(times, IATs, MWTs, AMBs, arm) {

    let arm_line_chart = null;
    //Remove previous arm charts
    switch (arm) {
        case 1:
            if (!!(document.getElementById('arm1_line_chart'))) {
                document.getElementById('arm1_line_chart').remove();
                let canvas = document.createElement('canvas');
                canvas.setAttribute("id", "arm1_line_chart");
                document.getElementById('arm1_line_chart_parent').appendChild(canvas);
            }
            arm_line_chart = document.getElementById('arm1_line_chart').getContext('2d');
            break;
        case 2:
            if (!!(document.getElementById('arm2_line_chart'))) {
                document.getElementById('arm2_line_chart').remove();
                let canvas = document.createElement('canvas');
                canvas.setAttribute("id", "arm2_line_chart");
                document.getElementById('arm2_line_chart_parent').appendChild(canvas);
            }
            arm_line_chart = document.getElementById('arm2_line_chart').getContext('2d');
            break;
        case 3:
            if (!!(document.getElementById('arm3_line_chart'))) {
                document.getElementById('arm3_line_chart').remove();
                let canvas = document.createElement('canvas');
                canvas.setAttribute("id", "arm3_line_chart");
                document.getElementById('arm3_line_chart_parent').appendChild(canvas);
            }
            arm_line_chart = document.getElementById('arm3_line_chart').getContext('2d');
            break;
        case 4:
            if (!!(document.getElementById('arm4_line_chart'))) {
                document.getElementById('arm4_line_chart').remove();
                let canvas = document.createElement('canvas');
                canvas.setAttribute("id", "arm4_line_chart");
                document.getElementById('arm4_line_chart_parent').appendChild(canvas);
            }
            arm_line_chart = document.getElementById('arm4_line_chart').getContext('2d');
            break;
    }


    // {#-------Oven_Temperature_PV--------#}
    let arm_time_list = times.split("_");
    let IAT_list = IATs.split("_");
    let MWT_list = MWTs.split("_");
    let AMB_list = AMBs.split("_");


    const timeFormat = 'h:mm:ss';


    const oven_temperature_chart = new Chart(arm_line_chart, {
        // The type of chart we want to create
        type: 'line',

        // The data for our dataset
        data: {
            labels: arm_time_list,
            datasets: [

                {
                    label: 'IAT (Probe Temperature)',
                    borderColor: window.chartColors.orange,
                    backgroundColor: 'transparent',
                    data: IAT_list,
                    fill: false,
                    pointRadius: 0,
                    borderWidth: 2,
                    spanGaps: false
                },
                {
                    label: 'MWT (Ambient Temperature)',
                    borderColor: window.chartColors.purple,
                    backgroundColor: 'transparent',
                    data: MWT_list,
                    fill: false,
                    pointRadius: 0,
                    borderWidth: 2,
                    spanGaps: false
                },
                {

                    label: 'AMB (Canister Internal Temperature)',
                    borderColor: window.chartColors.blue,
                    backgroundColor: 'transparent',
                    data: AMB_list,
                    fill: false,
                    pointRadius: 0,
                    borderWidth: 2,
                    spanGaps: false
                }]
        },

        //Configuration options go here
        options: {
            responsiveAnimationDuration: 0, // animation duration after a resize
            responsive: true,
            maintainAspectRatio: false,
            legend: {
                position: 'bottom',
                labels: {
                    padding: 10
                    // fontColor: window.chartColors.red,
                }
            },
            scales: {
                xAxes: [{
                    type: 'time',
                    distribution: 'linear', //data are spread at the same distance from each other
                    ticks: {
                        beginAtZero: false,
                        source: 'time',
                        autoSkip: true,
                        maxRotation: 0,
                        autoSkipPadding: 10
                    },
                    time: {
                        format: timeFormat,
                        unit: 'minute'
                    },
                    gridLines: {
                        display: true
                    }
                }],
                yAxes: [{
                    display: 'auto',
                    ticks: {
                        source: 'data',
                        autoSkip: false,
                        maxRotation: 0,
                        autoSkipPadding: 10
                    },

                    gridLines: {
                        display: true
                    }
                }]
            },
            hover: {
                animationDuration: 0 // duration of animations when hovering an item
            },
            layout: {
                padding: {left: 15, right: 15, top: 15, bottom: 15}
            },
            tooltips: {
                enabled: true,
                bodySpacing: 4,
                mode: "nearest",
                intersect: 0,
                position: "nearest",
                xPadding: 10,
                yPadding: 10,
                caretPadding: 10
            },
            plugins: {
                zoom: {
                    // Container for pan options
                    pan: {
                        // Boolean to enable panning
                        enabled: true,

                        // Panning directions. Remove the appropriate direction to disable
                        // Eg. 'y' would only allow panning in the y direction
                        mode: 'x'
                    },

                    // Container for zoom options
                    zoom: {
                        // Boolean to enable zooming
                        enabled: true,

                        // Zooming directions. Remove the appropriate direction to disable
                        // Eg. 'y' would only allow zooming in the y direction
                        mode: 'x',
                    }
                }
            }
        }
    });


}