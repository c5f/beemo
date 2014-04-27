'use strict';

// Dashboard controller for the Beemo current call snapshot dashboard.
app.controller('DashboardCtrl', function ($scope, Restangular) {

        // TODO: Remove this binding
        window.scope = $scope

        // Bind the call data to $scope.
        Restangular.setBaseUrl('/api/');
        $scope.dashboardCalls = [];

        // Bind the chart data to another $scope variable to render the chart.
        $scope.dashboardData = [{
            key: "Recent Calls",
            values: [[1,1],[2,0.8]]
        }];

        Restangular.all('calls').getList().
            then(function (calls) {
                calls = calls.slice(0, 50);

                $scope.dashboardCalls = calls;

                var dashboardData = calls.map(function (call, index) {
                    if (call.adherence_score != null) {
                        return [index, call.adherence_score];
                    } else {
                        return [index, 0];
                    }
                });

                $scope.dashboardData[0].values = dashboardData;
            });
    });
