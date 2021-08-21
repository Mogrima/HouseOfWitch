"use strict";

var gulp = require("gulp");
var sass = require('gulp-sass')(require('sass'));
var postcss = require("gulp-postcss");
var autoprefixer = require("autoprefixer");
const prefixer = require('gulp-autoprefixer');
var del = require("del");

gulp.task("css", function () {
  return gulp.src('scss/**/*.scss')
    .pipe(sass({outputStyle: 'compressed'}).on('error', sass.logError))
    .pipe(postcss([
      autoprefixer()
    ]))
    .pipe(gulp.dest('./shop/static/shop/css/'));
});

// function css() {
//   return gulp.src('scss/style.scss')
//     .pipe(sass({outputStyle: 'compressed'}).on('error', sass.logError))
//     .pipe(prefixer())
//     .pipe(gulp.dest('shop/static/shop/css/'));
// };

// exports.css = css;

//  gulp.task("clean", function () {
//   return del("./static/shop/css/");
//  });

 gulp.task("default", function () {

  gulp.watch("./scss/**/*.scss", gulp.series("css"));
});

// exports.default = gulp.parallel(
//   exports.css
//   )
