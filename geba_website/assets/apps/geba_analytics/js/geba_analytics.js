$(document).ready(function(){

    var endpoint = document.getElementById("DataContainer").getAttribute('url_endpoint');
    var data_values = [];
    var data_labels = [];

    $.ajax({
        url: endpoint,
        method: "GET",
        success: function(data){
            data_labels = data.labels,
            data_values = data.analytics_data,
            setChart()
        },
        error: function(error_data){
            console.log('Error!'),
            console.log(error_data)
        }
    })


function setChart(){
    var ctx = document.getElementById("myChart");
    var myChart = new Chart(ctx, {
        type: 'bar',
        data: {
        labels: data_labels,
        datasets: [{
            label: 'Daily Views',
            data: data_values,
            backgroundColor: [
                'rgba(255, 99, 132, 0.2)',
                'rgba(54, 162, 235, 0.2)',
                'rgba(255, 206, 86, 0.2)',
                'rgba(75, 192, 192, 0.2)',
                'rgba(153, 102, 255, 0.2)',
                'rgba(255, 159, 64, 0.2)'
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