'use strict';

angular.module('clientApp', [])
  .controller('MainCtrl', function ($scope, $http, $timeout, $document) {
    $scope.curr = '';

    function request_video(list, file) {
      var url = '/video/request/' + list + '/' + file.file;
      $http.get(url).success(function (res) {
        file.ready = true;
      }).error(function (res, status) {
        $timeout(function () {request_video(list, file)}, 2000, true);
      });
    };

    $scope.getCourseLists = function (course) {
      $http.get('/video/course/'+course+'/lists').then(function (res) {
        $scope.lists = res.data;
        $scope.select($scope.lists[0].name, $scope.lists[0].files[0]);
      });
    }


    $scope.select = function (list, file) {
      if (!file.ready) {
        request_video(list, file);
      } else {
        var video = $scope.filepath(list, file);
        $scope.curr = video;
        $scope.player.src = video;
        $scope.player.load();
        $scope.player.play();
      }
    };

    $scope.filepath = function (list, file) {
      return '/video/' + list + '/' + file.file;
    };

    function arr_del(arr, obj) {
      var idx = arr.indexOf(obj);
      if (idx > -1) {
        arr.splice(idx, 1);
      }
    };
  })
  .directive('player', function() {
    return {
      link: function (scope, element, attrs, controller) {
        scope.player = element[0];
        scope.player.volume = 0.2;
      }
    };
  });
