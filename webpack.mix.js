const mix = require('laravel-mix');

mix
    .js('src/app.js', 'build/app.js')
    .vue({version: 3})
    .browserSync({
        proxy: 'balancer.local',
        files: [
            'index.html',
            'build/*',
        ]
    })
;

