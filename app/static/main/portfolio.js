
let graph_prices = null;
let layout = null;
let current_stock = $("#stock_listing").first();
const CYCLE_TIME = 7500;
/*
Loads the detail of a stock using its stockid
stockid -- id of the stock
*/

function load_detail(stock_id) {
    $.ajax({
        data: { id: stock_id },
        type: 'POST',
        url: '/query_stock_info'
    }).done(function (data) {

        let name = data['corporate_name'];
        $('#stock_graph').text(name);

        graph_prices = [{
            x: data['dates'],
            y: data['prices'],
            mode: "lines"
        }];

        layout = {
            xaxis: { title: "Date", autorange: true },
            yaxis: { title: "Recorded Price", autorange: true },
            margin: {
                l: 75,
                r: 25,
                b: 75,
                t: 25,
                pad: 4
            }
        };

        Plotly.newPlot("price_plot", graph_prices, layout);

    }).fail(function () {
        console.log("Failed AJAX Call");
    });
}
/*
cycle to the next stock
after 7.5 seconds
*/

function cycle_next_stock() {
    current_stock = current_stock.next();
    if (current_stock.length == 0) {
        current_stock = $("#stock_listing").first();
    }
    current_stock.click();
}


$(window).resize(function () {
    Plotly.newPlot("price_plot", graph_prices, layout);
});


$(document).ready(function () {
    let num = $('#stock_listing').first().attr('value');
    load_detail(num);

    setInterval(function () {
        cycle_next_stock()
    }, CYCLE_TIME);
});