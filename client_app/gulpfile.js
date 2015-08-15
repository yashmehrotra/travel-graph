'use strict';

// Lib Imports
var gulp = require('gulp');
var clean = require('gulp-clean');
var concat = require('gulp-concat');
var uglify = require('gulp-uglify');
var rename = require('gulp-rename');
var less = require('gulp-less');
var changed = require('gulp-changed');
var watch = require('gulp-watch');
var plumber = require('gulp-plumber');
var ngAnnotate = require('gulp-ng-annotate');
var minifyHtml = require('gulp-minify-html');
var minifyCss = require('gulp-minify-css');

// File Paths
var paths = {
    build: {
        js: 'dist/js/',
        css: 'dist/css/',
        html: 'dist/html/'
    },
    js: 'public/js/**/*.js',
    css: 'public/css/*.less',
    html: 'public/views/*.html'
};

// Tasks
gulp.task('clean', function () {
    return gulp.src([paths.build.js, paths.build.html], {read: false})
        .pipe(clean({force: true}));
});

gulp.task('js', function() {
    return gulp.src(paths.js)
        .pipe(plumber())
        .pipe(changed(paths.js))
        .pipe(ngAnnotate())
        .pipe(concat('main.js'))
        .pipe(gulp.dest(paths.build.js))
        .pipe(uglify())
        .pipe(rename('main.min.js'))
        .pipe(gulp.dest(paths.build.js));
});

gulp.task('css', function () {
    return gulp.src(paths.css)
        .pipe(plumber())
        .pipe(changed(paths.css))
        .pipe(less())
        .pipe(concat('style.css'))
        .pipe(gulp.dest(paths.build.css))
        .pipe(minifyCss())
        .pipe(rename('style.min.css'))
        .pipe(gulp.dest(paths.build.css));
});

gulp.task('html', function() {
    return gulp.src(paths.html)
        .pipe(plumber())
        .pipe(changed(paths.html))
        .pipe(minifyHtml({empty: true}))
        .pipe(gulp.dest(paths.build.html));
});

gulp.task('watch', function() {
    gulp.watch(paths.js, ['js']);
    gulp.watch(paths.html, ['html']);
    gulp.watch(paths.css, ['css']);
});

gulp.task('default', ['clean'], function () {
    gulp.start('js', 'css', 'html', 'watch');
});
