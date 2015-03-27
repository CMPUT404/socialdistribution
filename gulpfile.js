var fs          = require('fs');
var gulp        = require('gulp');

var $           = require('gulp-load-plugins')();
var del         = require('del');
var source      = require('vinyl-source-stream');
var browserify  = require('browserify');
var runSequence = require('run-sequence');
var babelify    = require('babelify');
var babel       = require("gulp-babel");
var mocha       = require('gulp-mocha');

// require hook
require("babel/register");

var env = 'dev';

gulp.task('clean:dev', function() {
  return del(['.tmp']);
});

gulp.task('clean:dist', function() {
  return del(['dist']);
});

gulp.task('create-config', function(cb) {
  fs.writeFile('app/config.json', JSON.stringify({
    env: env,
  }), cb);
});

gulp.task('scripts', function() {
  var bundler = browserify('./app/scripts/app.js', {
    debug: true,
    extensions: ['.js','.jsx']
  }).transform(babelify);

  return bundler.bundle()
    .pipe(source('app.js'))
    .pipe(gulp.dest('.tmp/scripts'));
});

gulp.task('compass', function() {
  return gulp.src('app/styles/**/*.scss')
    .pipe($.plumber())
    .pipe($.compass({
      css: '.tmp/styles',
      sass: 'app/styles'
    }));
});

gulp.task('imagemin', function() {
  return gulp.src('app/images/*')
    .pipe($.imagemin({
            progressive: true,
            svgoPlugins: [{removeViewBox: false}]
    }))
    .pipe(gulp.dest('dist/images'));
});

gulp.task('copy', function() {
  return gulp.src(['app/*.txt', 'app/*.ico'])
    .pipe(gulp.dest('dist'));
});

gulp.task('bundle', function () {
  var assets = $.useref.assets({searchPath: '{.tmp,app,vendor}'});
  var jsFilter = $.filter(['**/*.js']);
  var cssFilter = $.filter(['**/*.css']);
  var htmlFilter = $.filter(['*.html']);

  return gulp.src('app/*.html')
    .pipe(assets)
    .pipe(assets.restore())
    .pipe($.useref())
    .pipe(jsFilter)
    .pipe($.uglify())
    .pipe(jsFilter.restore())
    .pipe(cssFilter)
    .pipe($.autoprefixer({
      browsers: ['last 5 versions']
    }))
    .pipe($.minifyCss())
    .pipe(cssFilter.restore())
    .pipe(htmlFilter)
    .pipe($.htmlmin({collapseWhitespace: true}))
    .pipe(htmlFilter.restore())
    .pipe(gulp.dest('dist'))
    .pipe($.size());
});

gulp.task('webserver', function() {
  return gulp.src(['.tmp', 'app', 'vendor'])
    .pipe($.webserver({
      host: 'localhost', //change to 'localhost' to disable outside connections
      livereload: true,
      open: true,
      port: 1337
    }));
});

gulp.task('serve', function() {
  runSequence('clean:dev', ['create-config', 'scripts', 'compass'], 'webserver');

  gulp.watch('app/*.html');

  gulp.watch('app/scripts/**/*.js', ['scripts']);

  gulp.watch('app/scripts/**/*.jsx', ['scripts']);

  gulp.watch('app/styles/**/*.scss', ['compass']);
});

gulp.task('build', function() {
  env = 'prod';

  runSequence(['clean:dev', 'clean:dist'],
              ['create-config', 'scripts', 'compass', 'imagemin', 'copy'],
              'bundle');
});

gulp.task('test', function () {
    return gulp.src('tests/**/*-test.js')
        .pipe(babel())
        .pipe(mocha({reporter: 'nyan'}));
});
