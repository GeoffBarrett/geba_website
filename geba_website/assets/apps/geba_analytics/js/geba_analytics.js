$(document).ready(function(){

    var endpoint = document.getElementById("DataContainer").getAttribute('url_endpoint');
    var data_values = [];
    var data_labels = [];

    $.ajax({
        url: endpoint,
        method: "GET",
        success: function(data){
            today_data_labels = data.today_labels
            today_data_values = data.today_data
            setTodayChart()

            daily_labels = data.daily_labels
            daily_data = data.daily_data
            daily_anon_data = data.daily_anon_data
            setDailyChart()

            monthly_labels = data.monthly_labels
            monthly_data = data.monthly_data
            monthly_anon_data = data.monthly_anon_data
            setMonthlyChart()
        },
        error: function(error_data){
            console.log('Error!'),
            console.log(error_data)
        }
    })


function setTodayChart(){
    var ctx = document.getElementById("todayViewedChart");
    var myChart = new Chart(ctx, {
        type: 'bar',
        data: {
        labels: today_data_labels,
        datasets: [{
            label: 'Today\'s Views',
            data: today_data_values,
            backgroundColor: [
                'rgba(255, 99, 132, 0.4)',
                'rgba(54, 162, 235, 0.4)',
                'rgba(255, 206, 86, 0.4)',
                'rgba(75, 192, 192, 0.4)',
                'rgba(153, 102, 255, 0.4)',
                'rgba(255, 159, 64, 0.4)'
            ],
            borderColor: [
                'rgba(255,99,132,1)',
                'rgba(54, 162, 235, 1)',
                'rgba(255, 206, 86, 1)',
                'rgba(75, 192, 192, 1)',
                'rgba(153, 102, 255, 1)',
                'rgba(255, 159, 64, 1)'
            ],
            borderWidth: 1
        }]
    },
    options: {
        responsive: true, // setting this value to false will make it so the height doesn't scale
        //maintainAspectRatio: false, // this will make it so it uses the width and height given
        scales: {
            yAxes: [{
                ticks: {
                    beginAtZero:true
                }
            }]
        }
    }
    });
}

function setDailyChart(){
    var ctx = document.getElementById("dailyViewedChart");
    var myChart = new Chart(ctx, {
        type: 'bar',
        data: {
        labels: daily_labels,
        datasets: [
        {
            label: 'Daily Views',
            backgroundColor: 'rgba(255, 99, 132, 0.4)',
            data: daily_data,
        },
        {
            label: 'Daily Anonymous Views',
            backgroundColor: 'rgba(54, 162, 235, 0.4)',
            data: daily_anon_data,
        }]
    },
    options: {
        responsive: true, // setting this value to false will make it so the height doesn't scale
        //maintainAspectRatio: false, // this will make it so it uses the width and height given
        scales: {
            yAxes: [{
                ticks: {
                    beginAtZero:true
                }
            }]
        }
    }
    });
}

function setMonthlyChart(){
    var ctx = document.getElementById("monthlyViewedChart");
    var myChart = new Chart(ctx, {
        type: 'bar',
        data: {
        labels: monthly_labels,
        datasets: [
        {
            label: 'Monthly Views',
            backgroundColor: 'rgba(255, 99, 132, 0.4)',
            data: monthly_data,
        },
        {
            label: 'Monthly Anonymous Views',
            backgroundColor: 'rgba(54, 162, 235, 0.4)',
            data: monthly_anon_data,
        }]
    },
    options: {
        responsive: true, // setting this value to false will make it so the height doesn't scale
        //maintainAspectRatio: false, // this will make it so it uses the width and height given
        scales: {
            yAxes: [{
                ticks: {
                    beginAtZero:true
                }
            }]
        }
    }
    });
}

});


