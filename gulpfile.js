'use strict';

// Lib Imports
var path = require('path');
var gulp = require('gulp');
var gutil = require('gulp-util');
var clean = require('gulp-clean');
var concat = require('gulp-concat');
var uglify = require('gulp-uglify');
var rename = require('gulp-rename');
var filesize = require('gulp-filesize');
var less = require('gulp-less');
var changed = require('gulp-changed');
var watch = require('gulp-watch');

// File Paths
var path_build = './travelgraph/static/build/';
var path_js = './travelgraph/static/js/**/*.js';
var path_less = './travelgraph/static/less/*.less';

// Tasks
gulp.task('clean', function () {
  return gulp.src(path_build, {read: false})
    .pipe(clean());
});

gulp.task('vendor', function() {
  return gulp.src(path_js)
    .pipe(concat('main.js'))
    .pipe(gulp.dest(path_build))
    .pipe(uglify())
    .pipe(rename('main.min.js'))
    .pipe(gulp.dest(path_build))
    .on('error', gutil.log)
});

gulp.task('css', function () {
  return gulp.src(path_less)
    .pipe(changed(path_build))
    .pipe(less({
      paths: [ path.join(__dirname, 'less', 'includes') ]
    }))
    .pipe(gulp.dest(path_build))
    .on('error', gutil.log);
});

gulp.task('css:watch', function () {
  watch({
    glob: path_less,
    emit: 'one',
    emitOnGlob: false
  }, function(files) {
    return files
      .pipe(less({
        paths: [ path.join(__dirname, 'less', 'includes') ]
      }))
      .pipe(gulp.dest(path_build))
      .on('error', gutil.log);
  });
});

gulp.task('default', ['clean'], function () {
  gulp.start('vendor');
  gulp.watch(path_js, ['vendor']);
});
