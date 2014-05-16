'use strict';

// Dashboard controller for the Beemo current call snapshot dashboard.
app.controller('DashboardCtrl', function ($scope) {

        // TODO: Remove this binding
        window.scope = $scope

        // Color function for the dashboard chart.
        $scope.dashboardColorFunction = function () {
            return function (element, index) {
                return "#428bca";
            }};

        // Bind the call data to $scope.
        $scope.dashboardCalls = [];

        // Bind the chart data to another $scope variable to render the chart.
        $scope.dashboardData = [];
    });
