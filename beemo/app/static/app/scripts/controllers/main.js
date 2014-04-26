'use strict';

app.controller('MainCtrl', function ($scope, Restangular) {

        window.scope = $scope;

        Restangular.setBaseUrl('/api/');

        // A list of the calls
        $scope.calls = [];

        $scope.awesomeThings = [
          'HTML5 Boilerplate',
          'AngularJS',
          'Karma'
        ];

        $scope.calls = Restangular.all('calls').getList();

        console.log();
    });
