// Sass configuration
var gulp = require('gulp');
var sass = require('gulp-sass');
var minify = require('gulp-minify-css');
var rename = require('gulp-rename');
var sourcemaps = require('gulp-sourcemaps');

gulp.task('sass', function() {
    gulp.src('ckanext/dadosabertos/public/sass/*.scss')
        .pipe(sourcemaps.init())
        .pipe(sass({ style: 'compressed' }))
        .pipe(rename({ extname: '.min.css' }))
        .pipe(minify())
        .pipe(sourcemaps.write('.'))
        .pipe(gulp.dest(function(f) {
            return f.base+"/../css/";
        }))
});

gulp.task('compile-scss', ['sass'], function() {
    gulp.watch('ckanext/dadosabertos/public/sass/*.scss', ['sass']);
})