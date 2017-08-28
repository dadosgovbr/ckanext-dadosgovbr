// Install requirements (nodejs, gulp) for Ubuntu 16.04
//      cd /usr/lib/ckan/default/src/ckanext-dadosgovbr
//      curl -sL https://deb.nodesource.com/setup_6.x | sudo -E bash -
//      sudo apt-get install -y build-essential nodejs
//      sudo npm install gulp-cli -g
//      sudo npm install gulp -D
//      sudo npm install node-sass
//      sudo npm install gulp-sass gulp-rename gulp-minify-css gulp-sourcemaps

// Sass configuration
var gulp = require('gulp');
var sass = require('gulp-sass');
var minify = require('gulp-minify-css');
var rename = require('gulp-rename');
var sourcemaps = require('gulp-sourcemaps');

gulp.task('sass', function() {
    gulp.src('ckanext/dadosgovbr/public/sass/*.scss')
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
    gulp.watch('ckanext/dadosgovbr/public/sass/*.scss', ['sass']);
})