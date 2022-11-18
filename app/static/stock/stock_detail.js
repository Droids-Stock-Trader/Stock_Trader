


function load_detail(stock_symbol, timeframe) {
    $.ajax({
        data: { symbol: stock_symbol, time: timeframe },
        type: 'POST',
        url: '/stock/stock_info'
    }).done(function (data) {

        raw_data = data['data'][stock_symbol]
        opened = []
        close_arr = []
        high = []
        low = []
        timestamps = []
        raw_data.forEach(element => {
            opened.push(element['open'])
            close_arr.push(element['close'])
            high.push(element['high'])
            low.push(element['low'])
            timestamps.push(element['timestamp'])
        });
        chart_parameters = [{
            x: timestamps,
            close: close_arr,
            decreasing: {line: {color: '#c23010'}},
            high: high,
            increasing: {line: {color: '#10c260'}}, 
            line: {color: 'rgba(31,119,180,1)'},
            low: low,
            open: opened,
            type: 'candlestick',
            xaxis: 'x',
            yaxis: 'y'
        }];

        var layout = {
            // dragmode: 'zoom', 
            margin: {
              r: 10, 
              t: 25, 
              b: 40, 
              l: 60
            }, 
            showlegend: false, 
            // xaxis: { title: "Date", autorange: true }, 
            yaxis: {
              title: "Price",
              domain: [0,1],
              range: [Math.min(opened),Math.max(close_arr)],
              cliponaxis: false, 
              type: 'linear'
            }
          };

        Plotly.newPlot("price_plot", chart_parameters, layout);

        var open_price = "Open price: " + raw_data.slice(-1)[0]['open']
        var close_price = "Close price : " + raw_data.slice(-1)[0]['close']
        $('#open_price').text(open_price);
        $('#close_price').text(close_price);

    }).fail(function () {
        console.log("Failed AJAX Call");
    });
}


$(window).resize(function () {
    Plotly.newPlot("price_plot", chart_parameters, layout);
});


function add_or_remove_stock(checkbox, symbol) {
    let add = null
    if (checkbox.checked) {
        add = 1
    } else {
        add = 0
    }

    $.ajax({
        data: {symbol: symbol, append: add}, 
        type: 'POST',
        url: '/stock/add_to_watch_list'
    }).done(function(reponse) {

    }).fail(function() {
        console.log("Failed AJAX Call")
    });
}