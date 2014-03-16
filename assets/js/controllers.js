'use strict';

/**
 * Magnus Persson 2014-03-09.
 */

var phonecatApp = angular.module('phonecatApp', []);

phonecatApp.controller('MonitCtrl', function ($scope, $http) {
    $http.get('/meta').then(function (res) {
        console.log(res.data);
        $scope.monits = res.data;
    });
});