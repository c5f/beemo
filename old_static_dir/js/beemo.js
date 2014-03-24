
// Override default Angular template tags:
var beemo = angular.module("Beemo", []).config(function($interpolateProvider) {
    $interpolateProvider.startSymbol('{$');
    $interpolateProvider.endSymbol('$}');
});


var calls = [];


$.getScript("/static/js/beemo_classes.js", function() {

    loadRecentCalls(renderRecentCalls);

});


var loadRecentCalls = function(callback) {
    var results;

    // Get the 50 most recent calls.
    $.getJSON( "/api/calls?page_size=50", function(data) {
        results = data["results"].reverse();
    })
    .done(function() {

        // Tranlate each result into a new Call object.
        $.each(results, function(index, object) {
            calls.push(new Call(object));
        });

        callback(calls);
    });
};


var renderRecentCalls = function(calls) {
    console.log("Render recent calls function called.");
    console.log("Found " + calls.length + " calls.");
};
