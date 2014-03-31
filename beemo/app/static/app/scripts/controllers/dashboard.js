'use strict';

// Dashboard controller for the Beemo current call snapshot dashboard.
app.controller('DashboardCtrl', function ($scope, Restangular) {

    // Setup
    Restangular.setBaseUrl('/api/');
    $scope.dashboardCalls = []

    $scope.dashboardCalls = Restangular.all('calls').getList().$object;
});
