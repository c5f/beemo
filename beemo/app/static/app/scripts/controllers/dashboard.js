'use strict';

// Dashboard controller for the Beemo current call snapshot dashboard.
app.controller('DashboardCtrl', function ($scope, Restangular) {

        // TODO: Remove this binding
        window.scope = $scope

        // Setup
        Restangular.setBaseUrl('/api/');
        $scope.dashboardCalls = []

        $scope.dashboardCalls = Restangular.all('calls').getList().$object;
    });
