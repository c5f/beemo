'use strict';

angular.module('beemoApp', [
  'ngRoute'
])
  .config(function ($routeProvider) {
    $routeProvider
      .when('/', {
        templateUrl: 'static/views/main.html',
        controller: 'MainCtrl'
      })
      .otherwise({
        redirectTo: '/static/'
      });
  });
