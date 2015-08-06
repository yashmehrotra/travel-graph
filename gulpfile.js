'use strict';

// requirements

var gulp = require('gulp'),
    browserify = require('gulp-browserify'),
    size = require('gulp-size'),
    clean = require('gulp-clean'),
    concat = require('gulp-concat'),
    rename = require('gulp-rename'),
    uglify = require('gulp-uglify');

// tasks

gulp.task('transform', function () {
  return gulp.src('./travelgraph/static/javascripts/main.js')
    .pipe(gulp.dest('./travelgraph/static/javascripts/src/'))
    .pipe(size());
});

gulp.task('uglify-minify', function() {
    return gulp.src('./travelgraph/static/javascripts/main.js')
        .pipe(uglify())
        .pipe(gulp.dest('./travelgraph/static/javascripts/src/main.js'));
});

gulp.task('clean', function () {
  return gulp.src(['./travelgraph/static/javascripts/src'], {read: false})
    .pipe(clean())
});

gulp.task('default', ['clean'], function () {
  gulp.start('transform');
  gulp.watch('./travelgraph/static/javascripts/main.js', ['transform']);
});
