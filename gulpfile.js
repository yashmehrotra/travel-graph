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

// File Paths
var paths = {
    build: {
        // all: './travelgraph/static/build/',
        js: './travelgraph/static/build/js/',
        less: './travelgraph/static/build/less/',
        html: './travelgraph/static/build/html/'
    },
    js: './travelgraph/static/js/**/*.js',
    less: './travelgraph/static/less/*.less',
    html: './travelgraph/static/partials/*.html'
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
    return gulp.src(paths.less)
        .pipe(plumber())
        .pipe(changed(paths.build.less))
        .pipe(less({
            paths: [ path.join(__dirname, 'less', 'includes') ]
        }))
        .pipe(gulp.dest(paths.build.less));
});

gulp.task('css:watch', function () {
    watch({
        glob: paths.less,
        emit: 'one',
        emitOnGlob: false
    }, function(files) {
        return files
            .pipe(plumber())
            .pipe(less({
                paths: [ path.join(__dirname, 'less', 'includes') ]
            }))
            .pipe(gulp.dest(paths.build.less));
    });
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
});

gulp.task('default', ['clean'], function () {
    gulp.start('js', 'html', 'watch');
});
