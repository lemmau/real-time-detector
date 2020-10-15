const path = require('path');
const HtmlWebpackPlugin = require('html-webpack-plugin');

module.exports = {
    entry: ['@babel/polyfill', './react/index.js'],
    output: {
        filename: 'build.js',
        path: path.join(__dirname, 'flask/static/'),
        publicPath: '/',
    },
    resolve: {
        extensions: ['.js', '.jsx'],
    },
    module: {
        rules: [
        {
            test: /\.m?js$/,
            use: {
                loader: 'babel-loader',
                options: {
                presets: ['@babel/preset-env', '@babel/preset-react']
                }
            }
        },      
        {
            test: /\.css$/i,
            use: ['css-loader'],
        },
        {
            test: /\.(png|svg|jpg|gif|mp3)$/,
            loader: 'file-loader',
        },
        ]
    },
    devServer: {
        historyApiFallback: true,
        public: "real-time-detector.com",
        port: 8080,
        https: true
    },
    plugins: [
        new HtmlWebpackPlugin({
            template: './react/index.html',
            filename: "index.html",
    }),
    ],
    externals: {
        'Config': JSON.stringify(require(path.join(__dirname, 'config/config.json'))),
    },
}
