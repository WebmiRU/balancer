const mix = require('laravel-mix');

mix
    .js('src/app.js', 'build/app.js')
    .vue({version: 3})
    .browserSync({
        proxy: 'balancer.local',
        port: 3003,
        files: [
            'index.html',
            'build/*',
        ]
    })
;

